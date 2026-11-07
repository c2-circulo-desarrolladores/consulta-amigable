from collections.abc import Iterable
from concurrent.futures import ThreadPoolExecutor, as_completed
from numbers import Integral
from pathlib import Path
from typing import Literal

import httpx2
import narwhals as nw
import requests
from bs4 import BeautifulSoup

from consulta_amigable.constants.config import Config, get_config
from consulta_amigable.steps.click import Search
from consulta_amigable.steps.workflow import Workflow
from consulta_amigable.utils.console import console
from consulta_amigable.utils.html import extract_states, has_search_panel
from consulta_amigable.utils.http import (
    MefSession,
    build_payload,
    build_search_payload,
    post_info,
)
from consulta_amigable.utils.parse_file import filename_save
from consulta_amigable.utils.tables import filter_content, html_table_to_dataframe


class MEFScraper:
    def __init__(
        self,
        steps: list,
        backend: Literal["pandas", "polars"] = "pandas",
        tipo: Literal["gasto", "ingreso"] = "gasto",
        act_proy: Literal["ActProy", "Actividad", "Proyecto"] = "ActProy",
        master_dir_save: str = "./data/mef/",
        convert_numeric: bool = True,
    ):
        if tipo not in ("gasto", "ingreso"):
            raise ValueError(f"Tipo '{tipo}' no válido. Use 'gasto' o 'ingreso'")

        raw_steps = list(steps)
        wk = Workflow(raw_steps)
        self._raw_steps = raw_steps
        self.tipo: Literal["gasto", "ingreso"] = tipo
        self.backend: Literal["pandas", "polars"] = backend
        self.steps = wk.p_steps
        self.master_dir_save = Path(master_dir_save)
        self.act_proy = act_proy
        self.convert_numeric = convert_numeric

        # Configuración que se establecerá al ejecutar run()
        self.year: int
        self.config: Config
        self.session: requests.Session
        self.url: str
        self.cols: list
        self.save_dir: Path

        # Resultados de la última ejecución
        self.years: list[int] = []
        self.runs: dict[int, "MEFScraper"] = {}
        self.errors: dict[int, Exception] = {}
        self.result: nw.DataFrame

    def run(
        self,
        year: int | Iterable[int],
        *,
        max_workers: int | None = None,
        raise_on_error: bool = False,
    ) -> "MEFScraper":
        """
        Ejecuta el scraping para un año o para varios.

        Args:
            year: Año (int) o iterable de años (list, tuple, range, ...).
            max_workers: Número máximo de hilos al pasar varios años.
                Por defecto se usa min(3, cantidad de años).
            raise_on_error: Si es True, lanza un error al final cuando algún año
                falló. Los resultados parciales quedan disponibles en `runs`,
                `errors` y `result`.

        Returns:
            La misma instancia con `result` (DataFrame combinado), `runs`
            (instancia por año) y `errors` (excepción por año).
        """
        max_workers = self._validate_max_workers(max_workers)
        years = self._normalize_years(year)

        self.years = years
        self.runs = {}
        self.errors = {}

        if len(years) == 1:
            self._run_single(years[0])
            self.runs = {years[0]: self}
            return self

        return self._run_multi(
            years,
            max_workers=max_workers,
            raise_on_error=raise_on_error,
        )

    @staticmethod
    def _normalize_years(year: int | Iterable[int]) -> list[int]:
        if isinstance(year, (bool, str, bytes)):
            raise TypeError("`year` debe ser un entero o un iterable de enteros")

        if isinstance(year, Integral):
            return [int(year)]

        try:
            iterator = iter(year)
        except TypeError:
            raise TypeError("`year` debe ser un entero o un iterable de enteros")

        # Deduplica y normaliza en una sola pasada
        years: list[int] = []
        seen: set[int] = set()
        for item in iterator:
            # Integral por si a alguien se le ocurre pasar una Serie de Pandas
            if isinstance(item, bool) or not isinstance(item, Integral):
                raise TypeError(f"El año {item!r} no es un entero")
            value = int(item)
            if value not in seen:
                seen.add(value)
                years.append(value)

        if not years:
            raise ValueError("Debes indicar al menos un año")

        return years

    @staticmethod
    def _validate_max_workers(max_workers: int | None) -> int | None:
        if max_workers is None:
            return None
        if isinstance(max_workers, bool) or not isinstance(max_workers, Integral):
            raise TypeError("`max_workers` debe ser un entero o None")
        if max_workers < 1:
            raise ValueError("`max_workers` debe ser mayor o igual a 1")
        return int(max_workers)

    def _spawn(self) -> "MEFScraper":
        """Crea una instancia nueva con la misma configuración."""
        return type(self)(
            self._raw_steps,
            backend=self.backend,
            tipo=self.tipo,
            act_proy=self.act_proy,
            master_dir_save=self.master_dir_save,
            convert_numeric=self.convert_numeric,
        )

    def _run_single(self, year: int) -> "MEFScraper":
        self._setup_config_year(year=year)

        result = self._process_step(
            mef=self.initial_session,
            step_idx=0,
            metadata={"year": [year]},
        )
        self.result = nw.concat(result)

        return self

    def _run_multi(
        self,
        years: list[int],
        *,
        max_workers: int | None = None,
        raise_on_error: bool = False,
    ) -> "MEFScraper":
        workers = max_workers or min(3, len(years))

        with ThreadPoolExecutor(max_workers=workers) as pool:
            futures = {
                pool.submit(self._spawn()._run_single, year): year for year in years
            }
            for future in as_completed(futures):
                year = futures[future]
                try:
                    self.runs[year] = future.result()
                except Exception as exc:
                    self.errors[year] = exc

        frames = [
            self.runs[year].result
            for year in sorted(self.runs)
            if self.runs[year].result is not None
        ]
        self.result = nw.concat(frames) if frames else None

        if self.errors:
            self._report_errors()
            if raise_on_error:
                details = "; ".join(
                    f"{year}: {exc}" for year, exc in sorted(self.errors.items())
                )
                raise RuntimeError(
                    f"Fallaron {len(self.errors)} año(s) de {len(years)}: {details}"
                )

        return self

    def _report_errors(self) -> None:
        failed = ", ".join(str(year) for year in sorted(self.errors))
        console.print(
            f"[yellow]Advertencia:[/yellow] fallaron {len(self.errors)} "
            f"año(s): {failed}. Revisa el atributo `errors` para más detalles."
        )

    def _do_post(
        self,
        mef: MefSession,
        grp,
        click_bttn,
        extras=None,
    ) -> MefSession:
        payload = build_payload(
            soup=mef.soup,
            year=self.year,
            state=mef.states,
            button_key=click_bttn,
            grp=grp,
            extras=extras or {},
            tipo=self.tipo,
            act_proy=self.act_proy,
        )

        return post_info(mef.client, self.config.url, payload, self.config.columns)

    def _already_saved(self, name_col, value):
        if name_col is None:
            return False
        path = filename_save(name=name_col, value=value, save_dir=self.save_dir)
        if path.exists():
            return True
        return False

    def _execute_search_step(self, mef: MefSession, post_step: Search) -> MefSession:
        """Ejecuta la búsqueda del paso sobre el estado actual, si la UI la ofrece."""
        if not has_search_panel(mef.soup):
            return mef

        search_payload = build_search_payload(
            mef.soup,
            year=self.year,
            state=mef.states,
            search_query=post_step.query,
            search_type=post_step.method,
            tipo=self.tipo,
            act_proy=self.act_proy,
        )
        return post_info(
            mef.client,
            self.config.url,
            search_payload,
            self.config.columns,
        )

    def _process_step(
        self,
        mef: MefSession,
        step_idx: int,
        metadata: dict,
    ) -> list[nw.DataFrame]:

        steps = self.steps
        is_final = step_idx + 1 == len(steps)
        columns = self.config.columns

        if step_idx >= len(steps):
            return []

        step = steps[step_idx]

        name_col = None

        as_col = step.click.as_column
        if as_col and step_idx >= 1:
            name_col = steps[step_idx - 1].click.name

        click_bttn = step.click.button
        text_search = step.rows.rows

        # should_save = step.save is not None
        post_step = step.search

        extras_params = {}

        # print(step)
        df_filtered = filter_content(mef.df, text_search)

        if len(df_filtered) == 0:
            raise ValueError(
                f"El paso {step_idx} ({step.click.button}) con filtro {text_search!r} "
                f"no encontró filas. \nColumnas disponibles: {mef.df.columns}."
                f"\nValores en '{columns[1]}': {mef.df[columns[1]].to_list()}"
            )
        results = []

        for row in df_filtered.iter_rows(named=True):
            grp = row.get(columns[0])
            current_meta = metadata.copy()
            current_value = row.get(columns[1])

            if name_col:
                current_meta[name_col] = [current_value]

            result_post = self._do_post(
                mef=mef,
                grp=grp,
                click_bttn=click_bttn,
                extras=extras_params,
            )

            if post_step is not None:
                result_post = self._execute_search_step(result_post, post_step)

            if is_final:
                last_name = step.click.name
                meta_values = {k: v[0] for k, v in current_meta.items()}

                child_df = (
                    result_post.df.with_columns(
                        **{k: nw.lit(v) for k, v in meta_values.items()}
                    )
                    .drop(columns[0])
                    .rename({columns[1]: last_name})
                )

                results.append(child_df)
            else:
                child = self._process_step(
                    mef=result_post,
                    step_idx=step_idx + 1,
                    metadata=current_meta,
                )
                results.extend(child)
        return results

    def _init_session(
        self,
        url: str,
        columns: list,
        convert: bool,
        backend: Literal["pandas", "polars"] = "polars",
    ) -> MefSession:
        """
        Inicializa la sesión HTTP y obtiene el estado inicial

        Args:
            url: URL del endpoint

        Returns:
            MefSession con la sesión, los estados y el dataframe iniciales
        """
        client = httpx2.Client()
        response = client.get(url, timeout=10)
        soup = BeautifulSoup(response.text, "html.parser")
        df = html_table_to_dataframe(
            soup, columns=columns, convert=convert, backend=backend
        )

        initial_states = extract_states(soup)

        initial_session = MefSession(
            client=client, states=initial_states, df=df, soup=soup
        )

        return initial_session

    def _setup_config_year(
        self,
        year: int,
    ):
        config = get_config(year, self.tipo)

        act_proy = self.act_proy

        if self.tipo == "gasto":
            if act_proy not in ["ActProy", "Actividad", "Proyecto"]:
                raise ValueError(
                    "Para `gasto` solo esta disponible: ActProy [default], Actividad, Proyecto"
                )
            url = config.url.format(year=year, ap=act_proy)
        else:
            url = config.url.format(year=year)

        # obtenermos la primera visita a la pagina en el anio n
        self.initial_session = self._init_session(
            url, config.columns, self.convert_numeric, self.backend
        )
        # obtnemos la metadata configurada para ese anio
        self.config = Config(range(1, 2), url, config.columns)
        self.year = year
        # Directorio específico del año
        self.save_dir = self.master_dir_save / self.tipo / str(year)
        self.save_dir.mkdir(parents=True, exist_ok=True)
