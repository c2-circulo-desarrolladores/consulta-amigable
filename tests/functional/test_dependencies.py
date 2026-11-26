import pytest

from consulta_amigable import BTN, ClickBtn, MEFScraper, Rows
from consulta_amigable.utils.dependencies import (
    OptionalDependencyMissingError,
    assert_optional_import,
)


def test_optional_dependency_disponible_no_falla():
    assert_optional_import("polars", extra="polars")
    assert_optional_import("pandas", extra="pandas")


def test_optional_dependency_faltante_sugiere_extra():
    # Nombre deliberadamente inexistente: simula una dependencia no instalada
    # sin tener que desinstalar polars/pandas del entorno.
    with pytest.raises(OptionalDependencyMissingError) as exc_info:
        assert_optional_import("paquete_inexistente_para_test", extra="polars")

    mensaje = str(exc_info.value)
    assert "consulta-amigable[polars]" in mensaje
    assert "uv add" in mensaje


def test_backend_invalido_falla_al_crear_scraper():
    steps = [Rows(["total"]), ClickBtn(BTN.NIVEL_GOBIERNO)]

    with pytest.raises(ValueError, match="Backend"):
        MEFScraper(steps, backend="duckdb")
