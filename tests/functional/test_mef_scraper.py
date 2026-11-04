import re

import pytest

from consulta_amigable import BTN, ClickBtn, MEFScraper, Rows


def test_boton_incorrecto_sugiere_boton_correcto():
    steps = [
        Rows(["total"]),
        ClickBtn(BTN.NIVEL_GOBIERNO),
        Rows(["locales"]),
        ClickBtn(BTN.GENERICA),
        Rows(["bienes y servicios"]),
        ClickBtn(BTN.DEPARTAMENTO),
    ]

    expected_msg = (
        "El botón 'ctl00$CPH1$BtnDepartamento' (BTN.DEPARTAMENTO) no existe o "
        "no se implementa en este paso. ¿Tal vez querías usar el botón "
        "'ctl00$CPH1$BtnDepartamentoMeta' (BTN.DEPARTAMENTO_META)?"
    )

    with pytest.raises(ValueError, match=re.escape(expected_msg)):
        MEFScraper(steps).run(2023)


def test_boton_departamento_meta_funciona():
    steps = [
        Rows(["total"]),
        ClickBtn(BTN.NIVEL_GOBIERNO),
        Rows(["locales"]),
        ClickBtn(BTN.GENERICA),
        Rows(["bienes y servicios"]),
        ClickBtn(BTN.DEPARTAMENTO_META),
    ]

    df = MEFScraper(steps).run(2023).result

    assert df is not None
    assert df.shape[0] > 0
