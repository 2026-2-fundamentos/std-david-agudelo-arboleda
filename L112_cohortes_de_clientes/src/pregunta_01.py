from pathlib import Path
import matplotlib.pyplot as plt
import pandas as pd


def build_cohort_analysis() -> pd.DataFrame:
    """
    Una tienda quiere saber si sus clientes vuelven a comprar después de su
    primera compra. Para responder, agrupe a los clientes en cohortes según
    el mes de su primera compra y mida, mes a mes, qué proporción de cada
    cohorte vuelve a comprar. Use `data/sales.csv.gz`, que tiene una fila por
    orden con su cliente (`CustomerID`) y su fecha (`OrderDate`).

    Use estas definiciones:

    - `cohort_month`: el mes de la primera compra del cliente, escrito como
      `AAAA-MM`.
    - `period_index`: los meses transcurridos desde `cohort_month`; es 0 en el
      mes de la primera compra, 1 en el mes siguiente, y así sucesivamente.
    - `active_customers`: la cantidad de clientes distintos de la cohorte que
      compraron en ese período.
    - `cohort_size`: la cantidad de clientes de la cohorte, es decir, sus
      clientes activos en el período 0.
    - `retention_rate`: `active_customers` sobre `cohort_size`.

    Genere dos archivos en `submission/`:

    1. `cohort_retention.csv`, sin el índice de Pandas, con las columnas
       `cohort_month`, `period_index`, `active_customers`, `cohort_size` y
       `retention_rate`, y una fila por cada combinación cohorte–período
       observada, ordenadas por cohorte y período.

    2. `cohort_retention_heatmap.png`, un mapa de calor de `retention_rate`
       con una fila por cohorte (eje vertical) y una columna por período
       (eje horizontal). Muestre los valores como porcentajes. Los períodos
       que todavía no se pueden observar para una cohorte no significan
       retención cero: déjelos vacíos en el mapa.

    La función también debe retornar la tabla de retención.

    Ejemplo del formato de `cohort_retention.csv`:

        cohort_month,period_index,active_customers,cohort_size,retention_rate
        2022-01,0,100,100,1.0
        2022-01,1,26,100,0.26
        ...
    """
    #df--
    df = pd.read_csv("data/sales.csv.gz")

    df["order_month"] = pd.to_datetime(df["OrderDate"]).dt.to_period("M")
    df["cohort_month"] = df.groupby("CustomerID")["order_month"].transform("min")
    #?
    df["period_index"] = (df["order_month"] - df["cohort_month"]).apply(lambda x: x.n)

    df["cohort_month"] = df["cohort_month"].astype(str)
    #print(df.head()  )
    #choorte--

    cohorte = (
        df.groupby(["cohort_month", "period_index"], as_index=False)["CustomerID"]
        .nunique()
        .rename(columns={"CustomerID": "active_customers"})
        .sort_values(["cohort_month", "period_index"])
    )

    cohorte["cohort_size"] = cohorte.groupby("cohort_month")["active_customers"].transform("first")

    cohorte["retention_rate"] = cohorte["active_customers"] / cohorte["cohort_size"]

    #------------------

    carpeta_salida = Path("submission")
    carpeta_salida.mkdir(parents=True, exist_ok=True)
    cohorte.to_csv(carpeta_salida / "cohort_retention.csv", index=False)


    #tabla-----------
    
    tabla_pivot = cohorte.pivot(index="cohort_month", columns="period_index", values="retention_rate") * 100
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.imshow(tabla_pivot.values, aspect="auto", cmap="Blues")
    ax.set_xticks(range(len(tabla_pivot.columns)))
    ax.set_xticklabels(tabla_pivot.columns)
    ax.set_yticks(range(len(tabla_pivot.index)))
    ax.set_yticklabels(tabla_pivot.index)
    ax.set_xlabel("period_index")
    ax.set_ylabel("cohort_month")
    for i in range(len(tabla_pivot.index)):
        for j in range(len(tabla_pivot.columns)):
            val = tabla_pivot.iloc[i, j]
            if pd.notna(val):
                ax.text(j, i, f"{val:.1f}%", ha="center", va="center")
    fig.tight_layout()
    fig.savefig(carpeta_salida / "cohort_retention_heatmap.png")
    plt.close(fig)

    return cohorte
