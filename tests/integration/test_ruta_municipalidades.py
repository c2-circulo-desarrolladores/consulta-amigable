"""
Obtiene todas las municipalidades
"""

import pytest

from consulta_amigable import BTN, ClickBtn, Rows
from consulta_amigable.scrapper import MEFScraper

# def assert_base_df(df: pl.DataFrame, columns: list):
#     assert list(df.select(pl.col("year")).unique()) == [2024]
#     # assert df.columns ==


@pytest.mark.integration
def test_ruta_municipalidades(data_dir):
    steps = [
        Rows(["total"]),
        ClickBtn(BTN.NIVEL_GOBIERNO),
        Rows(["locales"]),
        ClickBtn(BTN.GOB_LOCALES_MANCOMUNIDADES),
        Rows(["municipalidades"]),
        ClickBtn(BTN.DEPARTAMENTO),
        Rows(),
        ClickBtn(BTN.PROVINCIA),
        Rows(),
        ClickBtn(BTN.MUNICIPALIDAD),
    ]

    df = MEFScraper(steps, backend="polars").run(2025).result
    df.write_csv(data_dir / "municipalidades.csv")
