from pathlib import Path
import numpy as np
import pandas as pd


def pregunta_01() -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """
    Una entidad pública recibe peticiones, quejas, reclamos y sugerencias
    (PQRS) por dos canales, la página web y las cartas, y la ley le da 15 días
    hábiles para responder cada una. Su tarea es medir si la entidad cumple
    ese plazo.

    Los archivos `data/historical_requests_web.csv.gz` y
    `data/historical_requests_letter.csv.gz` tienen una fila por solicitud
    recibida entre 2016 y 2021 por cada canal, con su identificador
    (`record_id`), la fecha de entrada (`in_date`), el día de la semana de
    entrada (`day_name`) y la fecha de respuesta (`out_date`). Si `out_date`
    está vacía, la solicitud todavía no ha sido respondida.

    Tenga en cuenta lo siguiente:

    - Algunas solicitudes aparecen repetidas: elimine las filas idénticas
      dentro de cada canal, para contar cada solicitud una sola vez. Las
      filas sin `record_id` son solicitudes válidas.
    - Llame `letter` al canal de las cartas y `web` al de la página web.
    - Los días hábiles de respuesta son los días de lunes a viernes
      posteriores a la fecha de entrada, hasta la fecha de respuesta
      incluida. Por ejemplo, una solicitud que entra un viernes y se responde
      el lunes siguiente tardó 1 día hábil. No considere los festivos.
    - Los días calendario de respuesta son la diferencia entre la fecha de
      respuesta y la de entrada.
    - Una solicitud cumple el plazo si fue respondida en 15 días hábiles o
      menos. Una solicitud pendiente no ha cumplido el plazo.
    - `on_time_rate` es la proporción de solicitudes que cumplen el plazo,
      sobre el total de solicitudes, incluidas las pendientes.
    - Las medianas de días se calculan solamente con las solicitudes
      respondidas.

    Genere tres archivos en `submission/`, sin el índice de Pandas y con las
    columnas en el orden indicado:

    1. `channel_summary.csv`, con una fila por canal, en orden alfabético:
       `channel`, `requests`, `answered`, `pending`,
       `median_business_days` y `on_time_rate`.

    2. `yearly_summary.csv`, con una fila por año de entrada y canal,
       ordenada por año y luego por canal: `year`, `channel`, `requests`,
       `pending` y `on_time_rate`.

    3. `entry_day_summary.csv`, con una fila por día de entrada, de lunes a
       domingo, con los dos canales juntos: `day_name`, `requests`,
       `median_calendar_days` y `median_business_days`.

    Observe en el tercer archivo cómo cambia la lectura del tiempo de
    respuesta según se cuenten días calendario o días hábiles.

    La función también debe retornar las tres tablas, en el mismo orden.

    Ejemplo del formato de `channel_summary.csv`:

        channel,requests,answered,pending,median_business_days,on_time_rate
        letter,28138,...
        ...
    """
    #--
    cartas = pd.read_csv("data/historical_requests_letter.csv.gz").drop_duplicates()
    cartas["channel"] = "letter"

    #print(cartas.head())

    #--
    web = pd.read_csv("data/historical_requests_web.csv.gz").drop_duplicates()
    web["channel"] = "web"  

    #---

    df = pd.concat([cartas, web], ignore_index=True)

    fecha_in = pd.to_datetime(df["in_date"])

    fecha_out = pd.to_datetime(df["out_date"])
    respondidas = fecha_out.notna()

    #---

    df["year"] = fecha_in.dt.year
    df["pending"] = ~respondidas
    #print(df)
    df["calendar_days"] = (fecha_out - fecha_in).dt.days
    df["business_days"] = np.nan


    df.loc[respondidas, "business_days"] = np.busday_count(
        (fecha_in[respondidas] + pd.Timedelta(days=1)).values.astype("datetime64[D]"),
        (fecha_out[respondidas] + pd.Timedelta(days=1)).values.astype("datetime64[D]"),
    )


    df["on_time"] = respondidas & (df["business_days"] <= 15)

    #print(df.head())

    #------

    canales = df.groupby("channel", as_index=False).agg(
        requests=("channel", "size"),
        answered=("pending", lambda s: (~s).sum()),
        pending=("pending", "sum"),
        median_business_days=("business_days", "median"),
        on_time_rate=("on_time", "mean"),
    )

    anual = df.groupby(["year", "channel"], as_index=False).agg(
        requests=("channel", "size"),
        pending=("pending", "sum"),
        on_time_rate=("on_time", "mean"),
    )

    orden_dias = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    df["day_name"] = pd.Categorical(df["day_name"], categories=orden_dias, ordered=True)
    dias = df.groupby("day_name", observed=False, as_index=False).agg(
        requests=("day_name", "size"),
        median_calendar_days=("calendar_days", "median"),
        median_business_days=("business_days", "median"),
    )

    carpeta_salida = Path("submission")
    carpeta_salida.mkdir(parents=True, exist_ok=True)
    canales.to_csv(carpeta_salida / "channel_summary.csv", index=False)
    anual.to_csv(carpeta_salida / "yearly_summary.csv", index=False)
    dias.to_csv(carpeta_salida / "entry_day_summary.csv", index=False)

    return canales, anual, dias
