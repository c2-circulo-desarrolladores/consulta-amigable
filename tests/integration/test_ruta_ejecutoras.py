"""
Ruta para obtener todas las unidades ejecutoras a nivel nacional
"""

import pytest

from consulta_amigable import BTN, ClickBtn, Rows
from consulta_amigable.scraper import MEFScraper


@pytest.mark.integration
def test_ruta_ejecutoras(data_dir):
    steps = [
        Rows(["total"]),
        ClickBtn(BTN.NIVEL_GOBIERNO),
        Rows(["nacional"]),
        ClickBtn(BTN.SECTOR),
        Rows(),
        ClickBtn(BTN.PLIEGO),
        Rows(),
        ClickBtn(BTN.EJECUTORA),
    ]

    df = MEFScraper(steps, backend="pandas").run(2022).df
    df.to_csv(data_dir / "sector_salud.csv", index=False)
