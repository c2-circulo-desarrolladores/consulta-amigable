## [0.3.0] - 2026-11-28

### 🚀 Features

- Detecta cuando un backend se usa pero no está instalado - ([0ee945c](https://github.com/c2-circulo-desarrolladores/consulta-amigable.git/commit/0ee945c1d3f75175685e623f35ec5e23086ba50b))
- **(buttons)** Agrega botones de pliego y ejecutora - ([19dff1d](https://github.com/c2-circulo-desarrolladores/consulta-amigable.git/commit/19dff1dc261dc6eb823a6d8ab4cc569497c7280e))

### 🐛 Bug Fixes

- Quita pandas como backend por defecto - ([22ab454](https://github.com/c2-circulo-desarrolladores/consulta-amigable.git/commit/22ab45408dfe743d9b21a02635b03b8326a5d5c5))

### 🚜 Refactor

- Result -> df; añade type hints para df - ([a40f15d](https://github.com/c2-circulo-desarrolladores/consulta-amigable.git/commit/a40f15da76ff2431ee3ce1dd3e9a2d2536c5b5b0))

### 📚 Documentation

- Actualiza instalación y ejemplo rápido - ([3b751b9](https://github.com/c2-circulo-desarrolladores/consulta-amigable.git/commit/3b751b983292b07e471e42b43fb206a2a49b73ab))

### 🎨 Styling

- Runs ruff - ([a94e998](https://github.com/c2-circulo-desarrolladores/consulta-amigable.git/commit/a94e99889dad594a9d13457a291e646c292d289d))
- Runs ruff - ([3a3c5de](https://github.com/c2-circulo-desarrolladores/consulta-amigable.git/commit/3a3c5ded6e27ff83bb52d242661b0ed743c72b9c))
- Añade barras de progreso por año con rich - ([e47b4e0](https://github.com/c2-circulo-desarrolladores/consulta-amigable.git/commit/e47b4e0cf4e4851084a2d07648eafc5df08e2479))
- Runs ruff - ([56b290c](https://github.com/c2-circulo-desarrolladores/consulta-amigable.git/commit/56b290caad49ecfde5202757fcc1fe616a478218))

### 🧪 Testing

- Mejora tests de integración (salud y municipalidades) - ([e497b2d](https://github.com/c2-circulo-desarrolladores/consulta-amigable.git/commit/e497b2d5f1914046432558a7a6cecc8231e03add))
- Añade ruta_ejecutoras - ([05bf48e](https://github.com/c2-circulo-desarrolladores/consulta-amigable.git/commit/05bf48e6b43cab7b84a4a85fa2b9d605b076dca7))
- Añade test_quickstart - ([a369bb3](https://github.com/c2-circulo-desarrolladores/consulta-amigable.git/commit/a369bb3871ca0c0117384e08dd0515cb9072f01b))

### ⚙️ Miscellaneous Tasks

- Agrega pandas y polars como grupos opcionales de dependencias - ([b27fcb0](https://github.com/c2-circulo-desarrolladores/consulta-amigable.git/commit/b27fcb01ae7fc0209ca43e30414bad4c3c39346b))
- Mejora de tipos y limpia código muerto - ([69fdcde](https://github.com/c2-circulo-desarrolladores/consulta-amigable.git/commit/69fdcdeadaae0f8ef8fbd772ed810fff5773e56e))
- Drops support for python 3.10 - ([1e40c30](https://github.com/c2-circulo-desarrolladores/consulta-amigable.git/commit/1e40c30e60e0aa8744c7ad595354c1f5dd3d4e2e))
- Tests de integración solo corren para python 3.11 y 3.14 - ([482abb0](https://github.com/c2-circulo-desarrolladores/consulta-amigable.git/commit/482abb08897976a248beac575db00eef706d3843))

## [0.2.1] - 2026-11-07

### 💼 Other

- Version 0.2.0 -> 0.2.1 - ([2390e79](https://github.com/c2-circulo-desarrolladores/consulta-amigable.git/commit/2390e79d970820b698e88f17b4fd15746df0cf10))

### ⚙️ Miscellaneous Tasks

- Simplificar flujo de release.yml - ([3f85456](https://github.com/c2-circulo-desarrolladores/consulta-amigable.git/commit/3f854564d98f2a87e23a953b6559596a11cf12be))

## [0.2.0] - 2026-11-07

### 🚀 Features

- Reemplazar pandas por dataframe genérico para dejar que el usuario escoja el dataframe backend ([#4](https://github.com/c2-circulo-desarrolladores/consulta-amigable.git/issues/4)) - ([be718ff](https://github.com/c2-circulo-desarrolladores/consulta-amigable.git/commit/be718fff616ba38fd40ff05ca5453ba3943497a9))
- Run acepta uno o más años de manera concurrente ([#13](https://github.com/c2-circulo-desarrolladores/consulta-amigable.git/issues/13)) - ([ea48323](https://github.com/c2-circulo-desarrolladores/consulta-amigable.git/commit/ea48323e0afbf79a6ea15e1fec37d22d18525a19))

### 🐛 Bug Fixes

- **(utils)** Añadir error personalizado cuando un botón no existe en cierto paso y mostrar una sugerencia - ([06ac8ce](https://github.com/c2-circulo-desarrolladores/consulta-amigable.git/commit/06ac8ce77347363c42810c7cd71c218102a6d904))
- Añadir mensaje de error claro al encontrar error en process_step - ([53cbd3c](https://github.com/c2-circulo-desarrolladores/consulta-amigable.git/commit/53cbd3c361aaebd0c474c1aa170009336732525b))
- Añadir lowercase a filter_content - ([00be147](https://github.com/c2-circulo-desarrolladores/consulta-amigable.git/commit/00be1478743f702e25a39f7e7f1a2a30ad3de8bf))
- Dejar pandas como backend por defecto - ([fc43904](https://github.com/c2-circulo-desarrolladores/consulta-amigable.git/commit/fc439047cf2b3de1e07d6f9b737eee60780f24f3))
- **(constants)** Añadir botón de Provincia - ([16fd26e](https://github.com/c2-circulo-desarrolladores/consulta-amigable.git/commit/16fd26e3d92c69ebcf630ca788b2bb9f2767b75f))
- **(buttons)** Añadir botón de sector - ([84b1ce5](https://github.com/c2-circulo-desarrolladores/consulta-amigable.git/commit/84b1ce502a49a708311f4a4c283099e64e710d13))

### 🚜 Refactor

- Simplificar importaciones ([#3](https://github.com/c2-circulo-desarrolladores/consulta-amigable.git/issues/3)) - ([33ad5ae](https://github.com/c2-circulo-desarrolladores/consulta-amigable.git/commit/33ad5aefc47020915bcb68a71ff82237bf25620b))
- Añadir mejoras de tipado interno - ([f7dd27e](https://github.com/c2-circulo-desarrolladores/consulta-amigable.git/commit/f7dd27e82f4b0fee01f59125b6ae2b40180bce5d))
- Changes from requests.Session to httpx2.Client ([#9](https://github.com/c2-circulo-desarrolladores/consulta-amigable.git/issues/9)) - ([293087f](https://github.com/c2-circulo-desarrolladores/consulta-amigable.git/commit/293087f6fe3ceaac59845023e9d14a6476b2ae65))

### 📚 Documentation

- Actualiza README y configuración para CHANGELOGs - ([d35bb50](https://github.com/c2-circulo-desarrolladores/consulta-amigable.git/commit/d35bb50487ff814ca0c1dc9bc5907e28d4c7f58a))

### 🧪 Testing

- Agregar carpeta de tests para evaluar MefScraper, utils y workflow ([#5](https://github.com/c2-circulo-desarrolladores/consulta-amigable.git/issues/5)) - ([ad7db01](https://github.com/c2-circulo-desarrolladores/consulta-amigable.git/commit/ad7db01cb8b5570bb3e4e2cd1dee48874147e1e1))
- Adaptar test_utils para probar con pandas y polars como backends - ([bd2665d](https://github.com/c2-circulo-desarrolladores/consulta-amigable.git/commit/bd2665da9aeed2e1eeb510e2b04a530a946f8745))
- Añadir dos tests para probar que MefScraper funciona y otro que devuelva un error con sugerencia - ([a376437](https://github.com/c2-circulo-desarrolladores/consulta-amigable.git/commit/a376437c614ab0d4a2a986768e8e7bd0fd69cf91))
- Divide entre tests funciones y de integración - ([1fe493c](https://github.com/c2-circulo-desarrolladores/consulta-amigable.git/commit/1fe493cc4a09406711094fe0ab8370ecc76bf582))
- Añadir ruta de municipalidades - ([58815b1](https://github.com/c2-circulo-desarrolladores/consulta-amigable.git/commit/58815b154551b0cbdba471cc5086d2a206977d4f))
- Añadir test de integración concurrente para ruta salud - ([d89977b](https://github.com/c2-circulo-desarrolladores/consulta-amigable.git/commit/d89977b040896b5ed658300c95cb6304c91d1915))

### ⚙️ Miscellaneous Tasks

- Copiar archivos de PyPeruStats/MEF - ([08e5d85](https://github.com/c2-circulo-desarrolladores/consulta-amigable.git/commit/08e5d8575248302268b80cb8d8565f57bb913ba2))
- Añadir CODEOWNERS y setear a Jhon como rsponsable del repositorio - ([f183542](https://github.com/c2-circulo-desarrolladores/consulta-amigable.git/commit/f1835427a77f46a51777c07640000903ec402e8e))
- Añadir como dependencias requests, rich, narwhals, bs4 - ([e039cc7](https://github.com/c2-circulo-desarrolladores/consulta-amigable.git/commit/e039cc7b8a8718a9c6979902b9396bb0c93dcf12))
- Añadir pandas como dependencia dev - ([da71ad4](https://github.com/c2-circulo-desarrolladores/consulta-amigable.git/commit/da71ad4ced951c8026533ca8a8d3de555e596fb8))
- Mover _archive fuera del paquete - ([2718387](https://github.com/c2-circulo-desarrolladores/consulta-amigable.git/commit/27183879ff95b00d27943611afff2ed8455e3e0d))
- Crear grupo de dependencias test y comandos en el justfile para testear - ([4797f83](https://github.com/c2-circulo-desarrolladores/consulta-amigable.git/commit/4797f83c32c829a0daf4d8e6a6cea3fe26423536))
- Añadir workflows para format-check, release y test - ([c0e5b6a](https://github.com/c2-circulo-desarrolladores/consulta-amigable.git/commit/c0e5b6a8f7bdf254847d2b8e4124e96875c26f2c))
- Corregir workflow de test - ([d04b074](https://github.com/c2-circulo-desarrolladores/consulta-amigable.git/commit/d04b07443619b0bc59f7cae12d286dfb79b4080c))
- Actualizar dependencias y simplificar dependencias dev - ([c6ae293](https://github.com/c2-circulo-desarrolladores/consulta-amigable.git/commit/c6ae2932d2c342940a2fe069640b7e71603dabb1))
- Renombra scrapper -> scraper - ([34e8450](https://github.com/c2-circulo-desarrolladores/consulta-amigable.git/commit/34e8450e70f9bed29f5aa300d002f5b007e98233))
- Test workflow corre solo para PRs - ([ff6d51b](https://github.com/c2-circulo-desarrolladores/consulta-amigable.git/commit/ff6d51bf290c073decfe7276949c9d69200f2d8f))
- Añadir configuración de commitizen - ([d8c495b](https://github.com/c2-circulo-desarrolladores/consulta-amigable.git/commit/d8c495bcb5dea6a8ce8e8fc523c37e8ae8b2dd95))

