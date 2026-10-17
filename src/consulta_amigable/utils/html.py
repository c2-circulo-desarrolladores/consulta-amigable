"utils para manejar tablas"

from dataclasses import dataclass
from difflib import get_close_matches

from bs4 import BeautifulSoup

from ..constants import buttons as BTN

# print("asv")


@dataclass
class STATESHTML:
    _view_state: str
    _event_validation: str

    def _short(self, value: str) -> str:
        if not value:
            return ""
        if len(value) <= 5:
            return value
        return f"{value[:10]}...{value[-5:]}"

    def __repr__(self) -> str:
        return (
            f"STATESHTML("
            f"view_state='{self._short(self._view_state)}', "
            f"event_validation='{self._short(self._event_validation)}'"
            f")"
        )


def _btn_value_to_name_map() -> dict[str, str]:
    return {
        value: name
        for name, value in vars(BTN).items()
        if not name.startswith("_") and isinstance(value, str)
    }


def get_button_label(soup: BeautifulSoup, id_button_label: str) -> str:
    label = soup.find("input", {"name": id_button_label})
    if label is None:
        available_values: list[str] = [
            name
            for inp in soup.find_all("input")
            if (name := inp.get("name")) is not None
        ]

        suggestions = get_close_matches(
            id_button_label, available_values, n=1, cutoff=0.6
        )

        value_map = _btn_value_to_name_map()
        requested_name = value_map.get(id_button_label)
        requested_label = (
            f"'{id_button_label}' (BTN.{requested_name})"
            if requested_name
            else f"'{id_button_label}'"
        )

        msg = f"El botón {requested_label} no existe o no se implementa en este paso."

        if suggestions:
            suggested_value = suggestions[0]
            suggested_name = value_map.get(suggested_value, suggested_value)
            msg += (
                f" ¿Tal vez querías usar el botón "
                f"'{suggested_value}' (BTN.{suggested_name})?"
            )

        raise ValueError(msg)

    button_label = label.get("value")
    if button_label is not None:
        return button_label

    raise ValueError(
        f"El botón '{id_button_label}' existe pero no tiene atributo 'value' "
        "(no se puede interactuar con él)."
    )


def extract_states(soup: BeautifulSoup) -> STATESHTML:
    """
    Extrae los estados de ViewState y EventValidation del HTML

    Args:
        soup: BeautifulSoup object con el HTML

    Returns:
        Diccionario con __VIEWSTATE y __EVENTVALIDATION
    """
    viewstate = soup.select_one("#__VIEWSTATE")
    eventvalidation = soup.select_one("#__EVENTVALIDATION")
    states = STATESHTML(
        _view_state=viewstate["value"] if viewstate else "",
        _event_validation=eventvalidation["value"] if eventvalidation else "",
    )
    return states


def has_search_panel(soup: BeautifulSoup) -> bool:
    """
    Verifica si el HTML tiene el panel de búsqueda

    Busca el div con id="ctl00_CPH1_PnlSearch" que contiene:
    - Input de búsqueda: ctl00_CPH1_TxtSearch
    - Botón buscar por código: ctl00_CPH1_BtnSearchByCode
    - Botón buscar por descripción: ctl00_CPH1_BtnSearchByDescription

    Args:
        soup: BeautifulSoup del HTML

    Returns:
        True si existe el panel de búsqueda, False si no
    """
    search_panel = soup.find("div", {"id": "ctl00_CPH1_PnlSearch"})

    if not search_panel:
        return False

    # Verificar que existan los elementos de búsqueda
    search_input = soup.find("input", {"id": "ctl00_CPH1_TxtSearch"})
    btn_code = soup.find("a", {"id": "ctl00_CPH1_BtnSearchByCode"})
    btn_desc = soup.find("a", {"id": "ctl00_CPH1_BtnSearchByDescription"})

    return all([search_input, btn_code, btn_desc])
