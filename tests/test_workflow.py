from consulta_amigable import BTN, ClickBtn, Rows, Search
from consulta_amigable.steps.click import SavePartial
from consulta_amigable.steps.workflow import Step, Workflow

input = [
    Rows(["total"]),
    ClickBtn(BTN.NIVEL_GOBIERNO),
    ###############
    # click en la fila que tenga 'locales' y click en generica
    Rows(["locales"]),
    ClickBtn(BTN.GOB_LOCALES_MANCOMUNIDADES),
    ########
    Rows(["municipalidades"]),
    ClickBtn(BTN.GENERICA),
    ###############
    Rows(),
    # cuando no se define nada entonces se guarda la informacion de todas las filas y se iterara fila por fila los siguientes pasos
    ClickBtn(BTN.DEPARTAMENTO),
    # definimos el save partial para guardar progreso
    SavePartial(filename_prefix="departamento"),
    #############
    # solo estos departamentos
    Rows(["ica", "junin", "piura"]),
    ClickBtn(BTN.MUNICIPALIDAD),
    Search("provincial"),
]

output = [
    Step(
        rows=Rows(["total"]),
        click=ClickBtn(BTN.NIVEL_GOBIERNO),
    ),
    ###############
    # click en la fila que tenga 'locales' y click en generica
    Step(
        rows=Rows(["locales"]),
        click=ClickBtn(BTN.GOB_LOCALES_MANCOMUNIDADES),
    ),
    ########
    Step(
        rows=Rows(["municipalidades"]),
        click=ClickBtn(BTN.GENERICA),
    ),
    ###############
    Step(
        rows=Rows(),
        # cuando no se define nada entonces se guarda la informacion de todas las filas y se iterara fila por fila los siguientes pasos
        click=ClickBtn(BTN.DEPARTAMENTO),
        # definimos el save partial para guardar progreso
        save=SavePartial(filename_prefix="departamento"),
    ),
    #############
    Step(
        # solo estos departamentos
        rows=Rows(["ica", "junin", "piura"]),
        click=ClickBtn(BTN.MUNICIPALIDAD),
        search=Search("provincial"),
    ),
]


def test_workflow_builds_steps():
    workflow = Workflow(input)

    assert workflow.p_steps == output
