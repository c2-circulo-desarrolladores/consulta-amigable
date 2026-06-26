# MEF-CA
Consulta amigable del MEF

## Proyectos

- https://github.com/AlexEvanan/Web-Scraping-Consulta-Amigable-MEF
- https://github.com/TJhon/PyPeruStats/MEF
- https://github.com/rnicolasmr1998/Web_Scraping_Consulta_Amigable_MEF/tree/main/02_Script
- https://github.com/calderonsamuel/consulta_amigable_universidades

## Jhon

URL: - https://github.com/TJhon/PyPeruStats/MEF

> [!Note]
> Basado en peticiones HTTP, Trata de simular las acciones [click row, click button] (no estan todos los botones)

### Dependencias

```sh
pandas, requests, rich, bs4
```

### USO

```py
from perustats import MEFScraper
from perustats.MEF.constants import buttons as BTN
from perustats.MEF.steps.click import ClickBtn, Rows

steps = [
    Rows(["total"]),
    ClickBtn(BTN.NIVEL_GOBIERNO),
    Rows(["locales"]),
    ClickBtn(BTN.GENERICA),
    Rows(["bienes y servicios"]),
    ClickBtn(BTN.DEPARTAMENTO),
]

df = MEFScraper(steps).run(2023).result
print(df.head())
```

<img width="1462" height="310" alt="image" src="https://github.com/user-attachments/assets/a497e066-4949-42b4-b6e3-075cd0846746" />
