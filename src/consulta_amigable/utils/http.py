"""
utilities para hacer las peticiones al backend
"""

from dataclasses import dataclass

import httpx2
import narwhals as nw
from bs4 import BeautifulSoup

from consulta_amigable.utils.html import STATESHTML, extract_states, get_button_label
from consulta_amigable.utils.tables import html_table_to_dataframe


def build_search_payload(
    soup: BeautifulSoup,
    year: int,
    state: STATESHTML,
    search_query: str,
    search_type: str = "code",
    tipo: str = "gasto",
    act_proy: str = "ActProy",
) -> dict:
    """
    Construye el payload para una búsqueda (por código o descripción)

    Args:
        soup: BeautifulSoup del HTML actual
        year: Año
        state: Estados (ViewState, EventValidation)
        search_query: Texto a buscar
        search_type: "code" para búsqueda por código, "description" para descripción
        tipo: "gasto" o "ingreso"
        act_proy: Solo para gastos

    Returns:
        Diccionario con el payload para POST
    """
    # Determinar qué botón usar
    if search_type == "code":
        event_target = "ctl00$CPH1$BtnSearchByCode"
    elif search_type == "description":
        event_target = "ctl00$CPH1$BtnSearchByDescription"
    else:
        raise ValueError(
            f"search_type debe ser 'code' o 'description', recibido: {search_type}"
        )

    # Construir payload base
    payload = {
        "ctl00$CPH1$ScriptManager1": "ctl00$CPH1$UpdatePanel1|" + event_target,
        "__LASTFOCUS": "",
        "__EVENTTARGET": event_target,
        "__EVENTARGUMENT": "",
        "__VIEWSTATE": state._view_state,
        "__EVENTVALIDATION": state._event_validation,
        "ctl00$CPH1$DrpYear": str(year),
        "ctl00$CPH1$TxtSearch": search_query,
        "__ASYNCPOST": True,
    }

    # Solo agregar DrpActProy para gastos
    if tipo == "gasto":
        payload["ctl00$CPH1$DrpActProy"] = act_proy

    return payload


def build_payload(
    soup,
    year: int,
    state: STATESHTML,
    button_key: str,
    grp: str,
    extras: dict = None,
    tipo: str = "gasto",
    act_proy: str = "ActProy",
) -> dict:
    """
    Construye el payload para el POST

    Args:
        year: Año
        state: Estado (ViewState, EventValidation)
        button_key: Clave del botón a presionar
        grp: Código del grupo
        buttons: Diccionario de botones
        button_labels: Diccionario de labels
        extras: Parámetros adicionales (opcional)
        tipo: "gasto" o "ingreso"

    Returns:
        Diccionario con el payload completo
    """
    if extras is None:
        extras = {}
    base_payload = {
        "__EVENTTARGET": "",
        "__EVENTARGUMENT": "",
        "__VIEWSTATE": state._view_state,
        "__EVENTVALIDATION": state._event_validation,
        **extras,
        "ctl00$CPH1$DrpYear": year,
        button_key: get_button_label(soup, button_key),
        "grp1": grp,
    }

    # Solo agregar DrpActProy para gastos
    if tipo == "gasto":
        base_payload["ctl00$CPH1$DrpActProy"] = act_proy

    return base_payload


@dataclass
class MefSession:
    """Estado de una navegación: cliente HTTP + último HTML parseado."""

    client: httpx2.Client
    states: STATESHTML
    df: nw.DataFrame
    soup: BeautifulSoup


def post_info(
    session: httpx2.Client, url: str, payload: dict, columns: list
) -> MefSession:
    """
    Hace POST y retorna el nuevo estado de la navegación

    Args:
        session: Sesión de requests
        url: URL del endpoint
        payload: Datos del POST
        columns: Columnas esperadas en la tabla

    Returns:
        MefSession con la sesión, estados, dataframe y soup actualizados
    """
    response = session.post(url, data=payload, timeout=30)
    html = response.text

    soup = BeautifulSoup(html, "html.parser")
    states = extract_states(soup)
    df = html_table_to_dataframe(soup, columns=columns)
    return MefSession(client=session, states=states, df=df, soup=soup)


