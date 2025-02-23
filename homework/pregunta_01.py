"""
Escriba el codigo que ejecute la accion solicitada en la pregunta.
"""


def pregunta_01():
    """
    Realice la limpieza del archivo "files/input/solicitudes_de_credito.csv".
    El archivo tiene problemas como registros duplicados y datos faltantes.
    Tenga en cuenta todas las verificaciones discutidas en clase para
    realizar la limpieza de los datos.

    El archivo limpio debe escribirse en "files/output/solicitudes_de_credito.csv"

    """
    import pandas as pd
    import os


    data = pd.read_csv('./files/input/solicitudes_de_credito.csv', sep=";", index_col=0)
    cols = [
        "sexo",
        "tipo_de_emprendimiento",
        "idea_negocio",
        "monto_del_credito",
        "línea_credito",
    ]

    # Corrección de espaciado y caracteres especiales
    for col in cols:
        data[col] = (
            data[col].str.lower().str.strip().str.replace("_", " ").str.replace("-", " ").str.replace(",", "")
            .str.replace(".00", "").str.replace("$", "").str.strip()
        )

    # Corrección de mayúsculas y espaciado
    data["barrio"] = data["barrio"].str.lower().str.replace("_", " ").str.replace("-", " ")

    # Corrección de tipos de datos
    data["monto_del_credito"] = data["monto_del_credito"].astype(float)
    data["comuna_ciudadano"] = data["comuna_ciudadano"].astype(int)

    # Corrección de fechas
    data["fecha_de_beneficio"] = pd.to_datetime(
        data["fecha_de_beneficio"], format="%d/%m/%Y", errors="coerce"
    ).combine_first(
        pd.to_datetime(data["fecha_de_beneficio"], format="%Y/%m/%d", errors="coerce")
    )

    # Corrección de valores nulos y duplicados
    data = data.dropna()
    data = data.drop_duplicates()

    # Guardado de datos
    if not os.path.exists('./files/output'):
        os.makedirs('./files/output')
    data.to_csv("./files/output/solicitudes_de_credito.csv", sep=";", index=False)
pregunta_01()