"manejo de tablas"

import re
from typing import Literal

import narwhals as nw
from bs4 import BeautifulSoup

from consulta_amigable.utils.dependencies import assert_optional_import

_NUMBER_RE = re.compile(r"^[+-]?\d[\d,]*(?:\.\d+)?$")


def _parse_number(text: str) -> float | None:
    """Convierte un texto numérico a float; devuelve None si no es un número.

    Acepta separadores de miles, signo y paréntesis contables:
    ``"1,234.50"``, ``"-83,075,472"``, ``"(1,000.25)"``.
    """
    value = text.strip().replace("\u00a0", "").replace(" ", "")
    if not value:
        return None

    negative = value.startswith("(") and value.endswith(")")
    if negative:
        value = value[1:-1]

    if not _NUMBER_RE.match(value):
        return None

    number = float(value.replace(",", ""))
    return -number if negative else number


def filter_content(df: nw.DataFrame, rows: list | None = None) -> nw.DataFrame:
    if rows is None or len(rows) == 0:
        return df

    pattern = "|".join(map(re.escape, rows))
    df = df.filter(
        nw.col("concepto_region")
        .str.to_lowercase()
        .str.contains(pattern, literal=False)
    )
    return df


# TODO: Aquí utilizar ubigeos_peru
def html_table_to_dataframe(
    soup: BeautifulSoup,
    columns: list,
    backend: Literal["pandas", "polars"],
    convert: bool = True,
) -> nw.DataFrame:
    """
    Convierte la tabla HTML 'Data' en un DataFrame usando narwhals.

    Args:
        soup: BeautifulSoup object con el HTML
        columns: Lista de nombres de columnas
        backend: Backend narwhals a usar (ej. "polars", "pandas")
        convert: Si True, convierte números a float

    Returns:
        DataFrame (narwhals) con los datos de la tabla
    """
    if backend not in ("pandas", "polars"):
        raise ValueError(f"Backend '{backend}' no válido. Use 'pandas' o 'polars'")
    assert_optional_import(backend, extra=backend)

    table = soup.find("table", class_="Data")

    if table is None:
        raise ValueError("No se encontró la tabla 'Data' en el HTML")

    rows = []

    for tr in table.find_all("tr"):
        tds = tr.find_all("td")

        if not tds:
            continue

        row = []

        for i, td in enumerate(tds):
            text = td.get_text(strip=True)

            if i == 0:
                input_tag = td.find("input")
                if input_tag:
                    text = input_tag.get("value", text)

            row.append(text)

        rows.append(row)

    data: dict[str, list] = {}

    for i, col in enumerate(columns):
        values = [row[i] for row in rows]

        if convert:
            parsed = [_parse_number(v) if isinstance(v, str) else v for v in values]
            # Solo castear la columna si realmente contiene números. Así las
            # celdas vacías quedan como null en vez de mezclar str y float,
            # que en polars rompe la inferencia de tipos.
            if any(isinstance(v, float) for v in parsed):
                values = parsed

        data[col] = values

    df = nw.from_dict(data, backend=backend)

    return df


def get_grp_from_row(df: nw.DataFrame, row_index: int = 0) -> str:
    """
    Extrae el código grp de una fila específica del DataFrame

    Args:
        df: DataFrame con los datos
        row_index: Índice de la fila (por defecto 0)

    Returns:
        Código grp como string
    """
    if len(df) == 0:
        raise ValueError("DataFrame vacío")

    if row_index >= len(df):
        raise ValueError(
            f"Índice {row_index} fuera de rango. DataFrame tiene {len(df)} filas"
        )

    return df.select("codigo_grp").row(row_index)[0]


def find_row_by_text(df: nw.DataFrame, search_text: str) -> int:
    """
    Encuentra el índice de la primera fila que contiene el texto buscado

    Args:
        df: DataFrame con los datos
        search_text: Texto a buscar en la columna 'concepto_region'

    Returns:
        Índice de la fila encontrada

    Raises:
        ValueError: Si no se encuentra el texto
    """
    mask = (
        df["concepto_region"]
        .str.to_lowercase()
        .str.contains(search_text.lower(), literal=False)
        .fill_null(False)
    )

    matches = [i for i, val in enumerate(mask.to_list()) if val]

    if not matches:
        raise ValueError(f"No se encontró ninguna fila con el texto: '{search_text}'")

    return matches[0]
