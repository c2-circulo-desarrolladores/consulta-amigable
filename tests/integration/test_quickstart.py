"""
La ruta que está en el README
"""

import pytest

from consulta_amigable import BTN, ClickBtn, MEFScraper, Rows


@pytest.mark.integration
def test_quickstart(data_dir):
    steps = [
        Rows(["total"]),
        ClickBtn(BTN.NIVEL_GOBIERNO),
        Rows(["regionales"]),
        ClickBtn(BTN.SECTOR),
        Rows(["regionales"]),
        ClickBtn(BTN.PLIEGO),
    ]

    df = MEFScraper(steps, backend="pandas").run(2026).df
    df.to_csv(data_dir / "gobiernos_regionales_2026.csv", index=False)
    print(df.head())
