"manejo de tablas"

import re
from typing import Literal

import narwhals as nw
from bs4 import BeautifulSoup


def filter_content(df: nw.DataFrame, rows: list | None = None) -> nw.DataFrame:
    if rows is None or len(rows) == 0:
        return df

    pattern = "|".join(map(re.escape, rows))
    df = df.filter(nw.col("concepto_region").str.contains(pattern, literal=False))
    return df


def html_table_to_dataframe(
    soup: BeautifulSoup,
    columns: list,
    backend: Literal["pandas", "polars"] = "pandas",
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

            if convert and re.match(r"^[\d,]+\.?\d*$", text):
                text = text.replace(",", "")
                try:
                    text = float(text)
                except ValueError:
                    pass

            row.append(text)

        rows.append(row)

    data = {col: [row[i] for row in rows] for i, col in enumerate(columns)}

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
