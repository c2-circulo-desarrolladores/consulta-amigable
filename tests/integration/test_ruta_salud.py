"""
Ruta para obtener el gasto en salud desagregado por departamentos a lo largo de los años.
"""

import pytest

from consulta_amigable import BTN, ClickBtn, Rows
from consulta_amigable.scraper import MEFScraper

rango_años = range(2020, 2026)


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

    scraper = MEFScraper(steps, backend="polars").run(rango_años, raise_on_error=True)
    assert scraper.df is not None
    scraper.df.write_csv(data_dir / "sector_salud.csv")