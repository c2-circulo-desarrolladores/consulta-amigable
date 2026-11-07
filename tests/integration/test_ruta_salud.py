import pytest

from consulta_amigable import BTN, ClickBtn, Rows
from consulta_amigable.scraper import MEFScraper

# def assert_base_df(df: pl.DataFrame, columns: list):
#     assert list(df.select(pl.col("year")).unique()) == [2024]
#     # assert df.columns ==

@pytest.mark.integration
def test_ruta_salud(data_dir):
    steps = [
        Rows(["total"]),
        ClickBtn(BTN.NIVEL_GOBIERNO),
        Rows(["nacional"]),
        ClickBtn(BTN.SECTOR),
        Rows(["salud"]),
        ClickBtn(BTN.DEPARTAMENTO_META),
    ]

    df = MEFScraper(steps, backend="polars").run(2024).result
    df.write_csv(data_dir / "sector_salud.csv")

@pytest.mark.integration
def test_ruta_salud_concurrente(data_dir):
    steps = [
        Rows(["total"]),
        ClickBtn(BTN.NIVEL_GOBIERNO),
        Rows(["nacional"]),
        ClickBtn(BTN.SECTOR),
        Rows(["salud"]),
        ClickBtn(BTN.DEPARTAMENTO_META),
    ]

    df = MEFScraper(steps, backend="polars").run([2023, 2022]).result
    df.write_csv(data_dir / "sector_salud_concurrente.csv")
