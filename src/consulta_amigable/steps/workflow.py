from dataclasses import dataclass, field

from consulta_amigable.steps import ClickBtn, Rows, SavePartial, Search

STEPS = ClickBtn | Rows | SavePartial | Search


@dataclass
class Step:
    rows: Rows  # filtrar filas dentro de la tabla visible
    click: ClickBtn  # action
    save: SavePartial | None = None  # si guardamos el progreso desde este punto
    search: Search | None = (
        None  # accion adicional util cuando la tabla tiene muchisimos registros y se no aparece el elemento (el mef tiene su backen para este tipo de consulta -> busca por descripcion o codigo y actualiza la tabla)
    )


@dataclass
class Workflow:
    """
    helper: permite ordenar los pasos entendibles para el debugeo (para el desarrollador)
    """

    steps: list = field(default_factory=list)

    def __post_init__(self):
        self.p_steps = self._parse(self.steps)

    @staticmethod
    def _parse(raw: list[STEPS]) -> list[Step]:
        result = []
        i = 0
        while i < len(raw):
            item = raw[i]

            # Cada bloque debe comenzar con Rows
            if not isinstance(item, Rows):
                raise ValueError(
                    f"Se esperaba Rows en posición {i}, se obtuvo {type(item).__name__}"
                )

            rows = item
            click = save = search = None
            i += 1

            # Consumir los demás tipos del bloque hasta el próximo Rows (o fin)
            while i < len(raw) and not isinstance(raw[i], Rows):
                current = raw[i]
                if isinstance(current, ClickBtn):
                    click = current
                elif isinstance(current, SavePartial):
                    save = current
                elif isinstance(current, Search):
                    search = current
                else:
                    raise ValueError(
                        f"Tipo inesperado en posición {i}: {type(current).__name__}"
                    )
                i += 1

            if click is None:
                raise ValueError(f"Bloque con Rows({rows.rows}) no tiene ClickBtn")

            result.append(Step(rows=rows, click=click, save=save, search=search))

        return result
