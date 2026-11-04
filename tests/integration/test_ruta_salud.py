from pathlib import Path

from consulta_amigable import BTN, ClickBtn, Rows, Search
from consulta_amigable.scrapper import MEFScraper
from consulta_amigable.steps.click import SavePartial
from consulta_amigable.steps.workflow import Step, Workflow
import polars as pl

ROOT = Path(__file__).parent.parent / "data"

def assert_base_df(df: pl.DataFrame, columns: list):
    assert list(df.select(pl.col("year")).unique()) == [2024]
    # assert df.columns == 


def test_ruta_salud():
    steps = [
        Rows(["total"]),
        ClickBtn(BTN.NIVEL_GOBIERNO),
        Rows(["locales"]),
        ClickBtn(BTN.GOB_LOCALES_MANCOMUNIDADES),
        Rows(["municipalidades"]),
        ClickBtn(BTN.DEPARTAMENTO),
        ###############
        Rows(),
        ClickBtn(BTN.PROVINCIA),
        # # solo estos departamentos
        # Rows(),
        # ClickBtn(BTN.MUNICIPALIDAD),
    ]

    df = MEFScraper(steps, backend="polars").run(2024).result
    df.write_csv(ROOT / "test.csv")

