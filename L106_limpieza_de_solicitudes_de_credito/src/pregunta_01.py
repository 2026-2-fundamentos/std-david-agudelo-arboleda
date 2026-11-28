from pathlib import Path
import pandas as pd


def pregunta_01():
    """
    El archivo `data/solicitudes_de_credito.csv.gz` contiene las solicitudes de
    un programa de crédito, pero llegó sucio: tiene una columna de índice que
    no pertenece a los datos, registros duplicados, registros incompletos y
    valores que representan lo mismo escritos de formas distintas en los
    campos de texto, las fechas, el estrato y el monto.

    Su tarea es limpiarlo y guardar el resultado en
    `submission/solicitudes_de_credito.csv`, usando punto y coma (`;`) como
    separador y sin el índice de Pandas.

    El archivo limpio debe cumplir lo siguiente:

    - Contiene solamente las nueve columnas `sexo`, `tipo_de_emprendimiento`,
      `idea_negocio`, `barrio`, `estrato`, `comuna_ciudadano`,
      `fecha_de_beneficio`, `monto_del_credito` y `línea_credito`, en ese
      orden.
    - Los campos de texto están en minúsculas y sus palabras separadas por
      espacios.
    - `estrato` y `monto_del_credito` son números enteros, sin símbolos ni
      separadores de miles.
    - Todas las fechas de `fecha_de_beneficio` usan un mismo formato, por
      ejemplo `AAAA-MM-DD`.
    - No hay registros incompletos. La única excepción es
      `comuna_ciudadano`: sus valores faltantes son parte de los datos
      originales y deben conservarse.
    - No hay registros duplicados.

    Ejemplo del formato del archivo:

        sexo;tipo_de_emprendimiento;idea_negocio;barrio;estrato;...
        femenino;comercio;almacen de ropa en;los cerros el vergel;2;...
        ...
    """
    columnas = [
        "sexo",
        "tipo_de_emprendimiento",
        "idea_negocio",
        "barrio",
        "estrato",
        "comuna_ciudadano",
        "fecha_de_beneficio",
        "monto_del_credito",
        "línea_credito",
    ]
    columnas_texto = [
        "sexo",
        "tipo_de_emprendimiento",
        "idea_negocio",
        "barrio",
        "línea_credito",
    ]

    df = pd.read_csv(
        "data/solicitudes_de_credito.csv.gz", sep=";", index_col=0
    )
    df = df[columnas]
    df = df.dropna(subset=[col for col in columnas if col != "comuna_ciudadano"])

    for col in columnas_texto:
        df[col] = (
            df[col]
            .astype(str)
            .str.lower()
            .str.replace("_", " ", regex=False)
            .str.replace("-", " ", regex=False)
            .str.strip()
        )

    df["estrato"] = df["estrato"].astype(int)
    df["comuna_ciudadano"] = df["comuna_ciudadano"].astype("Int64")
    df["monto_del_credito"] = (
        df["monto_del_credito"]
        .astype(str)
        .str.replace(r"[$,\s]", "", regex=True)
        .astype(float)
        .astype(int)
    )

    fechas = pd.to_datetime(
        df["fecha_de_beneficio"], format="%d/%m/%Y", errors="coerce"
    )
    for fmt in ["%Y-%m-%d", "%Y/%m/%d"]:
        fechas = fechas.fillna(
            pd.to_datetime(df["fecha_de_beneficio"], format=fmt, errors="coerce")
        )
    df["fecha_de_beneficio"] = fechas.dt.strftime("%Y-%m-%d")

    df = df.drop_duplicates()

    carpeta_salida = Path("submission")
    carpeta_salida.mkdir(parents=True, exist_ok=True)
    df.to_csv(carpeta_salida / "solicitudes_de_credito.csv", sep=";", index=False)
