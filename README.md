<div align="center">

# 🏦 MEF — Consulta Amigable del Presupuesto Público

*API de Python no oficial para automatizar la extracción de datos del portal **Consulta Amigable** del Ministerio de Economía y Finanzas (MEF) del Perú.*

[![Python Version](https://img.shields.io/badge/python-3.12%2B-blue.svg)](https://www.python.org/)
[![Package Manager](https://img.shields.io/badge/uv-managed-purple.svg)](https://github.com/astral-sh/uv)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

</div>


El paquete **`consulta_amigable`** ofrece una API de Python no oficial para automatizar la extracción de datos del portal **Consulta Amigable** del Ministerio de Economía y Finanzas (MEF) del Perú. Cubre datos de **gasto** y de **ingreso** desde 2009 en adelante.


## ¿Qué es la Consulta Amigable?

[Consulta Amigable](https://apps5.mineco.gob.pe/transparencia/Navegador/Navegar_7.aspx) es el portal de transparencia pública del MEF, donde ciudadanos e investigadores pueden explorar la ejecución presupuestal del Perú. Expone una interfaz jerárquica que permite navegar por niveles de gobierno, regiones geográficas, categorías presupuestales y más.

`consulta_amigable` reemplaza la navegación manual de clics con una **API declarativa basada en pasos** que refleja el flujo de interacción humana.


## Características principales

- ✅ **Flujo de trabajo declarativo**: describe los pasos de navegación en Python simple; el scraper se encarga de las peticiones HTTP, el parseo de HTML y la paginación.
- ✅ **Gasto e ingreso**: consulta ambos conjuntos de datos.
- ✅ **Soporte multianual**: datos desde 2009 hasta el presente, con detección automática de la versión de la plataforma (v4 → v7).
- ✅ **Filtrado difuso de filas**: usa fragmentos de texto para coincidir filas sin necesitar el texto exacto.
- ✅ **Soporte del panel de búsqueda**: maneja tablas grandes (400+ filas) mediante la API de búsqueda integrada del MEF.
- ✅ **Salida compatible con pandas y polars**: los resultados se devuelven como DataFrames de narwhals listos para analizar.
- 🔜 **Guardado parcial**: guarda el progreso en disco durante el scraping _(próximamente)_.
- 🔜 **Barras de progreso**: retroalimentación visual para flujos largos _(próximamente)_.


## Instalación

```bash
pip install consulta-amigable
```


## Ejemplo rápido

```python
from consulta_amigable import BTN, ClickBtn, MEFScraper, Rows

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


## Estructura del módulo

```
consulta_amigable/
├── __init__.py          # API pública
├── scraper.py           # MEFScraper — orquesta el flujo completo
├── constants/
│   ├── buttons.py       # Constantes de ID de botones (BTN.*)
│   ├── config.py        # URLs y configuración de columnas por versión
│   ├── reference.py     # Plantillas de URL y cabeceras HTTP
│   └── tables.py        # Listas de nombres de columnas por versión
├── steps/
│   ├── click.py         # Primitivas Rows, ClickBtn, Search y SavePartial
│   └── workflow.py      # Parser de Workflow — convierte listas planas en Step
└── utils/               # Helpers internos de HTTP, HTML y parseo (no API pública)
```


## Navegación

- [Guía rápida](#guía-rápida): guía paso a paso para tu primera consulta.
- [Concepto básico: pasos](#concepto-básico-pasos): cómo se modela la navegación del MEF.
- [Tu primera consulta](#tu-primera-consulta): ejemplo completo desde cero.
- [Elegir gasto o ingreso](#elegir-gasto-o-ingreso): cambia entre gasto e ingreso.
- [Filtrar filas](#filtrar-filas): filtrado difuso con `Rows`.
- [La bandera `as_column`](#la-bandera-as_column): controla las columnas de metadata.
- [Manejar tablas grandes con `Search`](#manejar-tablas-grandes-con-search): usa el buscador del MEF.
- [Seleccionar `act_proy`](#seleccionar-act_proy): actividades y proyectos.
- [Ejemplo completo](#ejemplo-completo): receta real de scraping.
- [Próximos pasos](#próximos-pasos): recursos adicionales.


## Guía rápida

Esta guía te acompaña en la instalación de `consulta-amigable` y en la ejecución de tu primera consulta al MEF en menos de cinco minutos.

Las dependencias principales (`httpx2`, `beautifulsoup4`, `narwhals`, `requests` y `rich`) se instalan automáticamente. Para trabajar con los DataFrames, instala el backend que prefieras, por ejemplo `pandas` o `polars`.


### Concepto básico: pasos

El portal del MEF funciona como un navegador de tipo drill-down: haces clic en un botón para cargar una nueva tabla, seleccionas una fila, haces clic en otro botón, y así sucesivamente. `consulta_amigable` modela esto como una **lista plana de pares alternados `Rows` → `ClickBtn`** que el parser de `Workflow` convierte internamente en objetos `Step`.

```
[Rows(filtro), ClickBtn(botón), Rows(filtro), ClickBtn(botón), ...]
```

Cada par significa: *"filtra la tabla actual a las filas que coincidan con estas palabras clave y luego haz clic en este botón."*


### Tu primera consulta

#### 1. Importa las piezas

```python
from consulta_amigable import BTN, ClickBtn, MEFScraper, Rows
```

#### 2. Define tus pasos de navegación

```python
steps = [
    Rows(["total"]),              # empieza en la fila "Total"
    ClickBtn(BTN.NIVEL_GOBIERNO), # clic en "Nivel de Gobierno"
    Rows(["locales"]),            # selecciona "Gobiernos Locales"
    ClickBtn(BTN.GENERICA),       # clic en "Genérica de Gasto"
    Rows(["bienes y servicios"]), # filtra a "Bienes y Servicios"
    ClickBtn(BTN.DEPARTAMENTO),   # último nivel: por departamento
]
```

#### 3. Ejecuta el scraper

```python
scraper = MEFScraper(steps)
result = scraper.run(2023)

print(result.result)
```

`result.result` es un DataFrame con las columnas de ejecución presupuestal para cada departamento.


### Elegir gasto o ingreso

Por defecto, `MEFScraper` consulta **gasto**. Para consultar **ingreso**:

```python
scraper = MEFScraper(steps, tipo="ingreso")
```


### Filtrar filas

`Rows` acepta una lista de **fragmentos de texto que se buscan sin distinguir mayúsculas de minúsculas**. Se conserva toda fila cuyo texto contenga al menos uno de los fragmentos. Pasa una **lista vacía** (o simplemente `Rows()`) para recorrer *todas* las filas:

```python
Rows(["ica", "junin", "piura"])  # solo estos tres departamentos
Rows()                            # todas las filas de la tabla
```


### La bandera `as_column`

Por defecto, `ClickBtn` registra el valor de cada fila visitada como una columna adicional de metadata en el DataFrame final. Usa `as_column=False` cuando quieras navegar por un nivel sin registrarlo:

```python
ClickBtn(BTN.GOB_LOCALES_MANCOMUNIDADES, as_column=False)
```


### Manejar tablas grandes con `Search`

Cuando una tabla supera las ~400 filas, el portal del MEF oculta entradas y muestra un cuadro de búsqueda. Usa `Search` inmediatamente después de un `ClickBtn` para enviar una consulta al backend del MEF antes de que se ejecute el siguiente filtro `Rows`:

```python
steps = [
    ...
    Rows(["locales"]),
    ClickBtn(BTN.MUNICIPALIDAD),
    Search("provincial"),          # busca "provincial" en la descripción
    Rows(["lima"]),
    ClickBtn(BTN.GENERICA),
]
```


### Seleccionar `act_proy`

Para consultas de gasto, puedes alternar entre *Actividades/Proyectos*, *solo Actividades* o *solo Proyectos*:

```python
MEFScraper(steps, act_proy="Actividad")   # por defecto: "ActProy"
MEFScraper(steps, act_proy="Proyecto")
```


### Ejemplo completo

```python
from consulta_amigable import BTN, ClickBtn, MEFScraper, Rows

# Gasto en bienes y servicios de gobiernos locales, desagregado por departamento
steps = [
    Rows(["total"]),
    ClickBtn(BTN.NIVEL_GOBIERNO),
    Rows(["locales"]),
    ClickBtn(BTN.GOB_LOCALES_MANCOMUNIDADES, as_column=False),
    Rows(["municipal"]),
    ClickBtn(BTN.GENERICA),
    Rows(["bienes y servicios", "deuda publica"]),
    ClickBtn(BTN.DEPARTAMENTO),
    Rows(["ancash", "lima"]),
    ClickBtn(BTN.MUNICIPALIDAD),
]

df = MEFScraper(steps, convert_numeric=True).run(2022).result
print(df)
```


### Próximos pasos

- [Concepto básico: pasos](#concepto-básico-pasos): cómo se modela la navegación.
- [Filtrar filas](#filtrar-filas): filtrado difuso con `Rows`.
- [Manejar tablas grandes con `Search`](#manejar-tablas-grandes-con-search): búsqueda en el servidor.
- [Ejemplo completo](#ejemplo-completo): receta real de scraping.
- [Constantes de botones](src/consulta_amigable/constants/buttons.py): IDs de botones disponibles.
