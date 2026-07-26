from consulta_amigable import BTN, ClickBtn, MEFScraper, Rows


def main():
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


main()
