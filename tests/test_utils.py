import narwhals as nw
import pytest
from bs4 import BeautifulSoup

from consulta_amigable.utils.tables import html_table_to_dataframe

html = """
<table class="Data">
    <tr>
        <td><input value="001"/></td>
        <td>Transferencias de capital al Gobierno Regional de Lima</td>
        <td>1,200,000.50</td>
    </tr>
    <tr>
        <td><input value="002"/></td>
        <td>Gasto corriente en educación básica en Cusco</td>
        <td>850,300.00</td>
    </tr>
    <tr>
        <td><input value="003"/></td>
        <td>Inversión en infraestructura vial en Arequipa</td>
        <td>2,500,100.75</td>
    </tr>
    <tr>
        <td><input value="004"/></td>
        <td>Programa social en la región Puno</td>
        <td>430,000.00</td>
    </tr>
</table>
"""
soup = BeautifulSoup(html, "html.parser")
columns = ["codigo", "concepto_region", "monto"]


@pytest.mark.parametrize("backend", ["pandas", "polars"])
def test_html_table_to_dataframe(backend):
    df = html_table_to_dataframe(soup, columns=columns, backend=backend)

    assert isinstance(df, nw.DataFrame)

    # Shape
    assert df.shape == (4, 3)

    # Column names
    assert df.columns == columns

    # Values
    assert df["concepto_region"].to_list() == [
        "Transferencias de capital al Gobierno Regional de Lima",
        "Gasto corriente en educación básica en Cusco",
        "Inversión en infraestructura vial en Arequipa",
        "Programa social en la región Puno",
    ]

    assert df["monto"].to_list() == [
        1200000.50,
        850300.00,
        2500100.75,
        430000.00,
    ]
