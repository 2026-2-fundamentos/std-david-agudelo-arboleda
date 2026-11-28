from pathlib import Path
import pandas as pd


def pregunta_01() -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """
    Una cadena de suministros de oficina vende mucho, pero la gerencia
    sospecha que parte de esas ventas no deja utilidad. El archivo
    `data/superstore_orders.csv.gz` tiene una fila por línea de pedido, con
    el número de pedido (`Order ID`), las ventas (`Sales`), la utilidad
    (`Profit`), el descuento aplicado (`Discount`, como proporción), el
    segmento del cliente (`Customer Segment`) y la categoría del producto
    (`Product Category`). Una utilidad negativa significa que la línea se
    vendió con pérdida.

    Use estas definiciones:

    - Margen (`profit_margin`): utilidad sobre ventas.
    - Línea con pérdida: una línea cuya utilidad es negativa.
    - `loss_line_rate`: la proporción de líneas con pérdida.
    - `lost_profit`: la suma de las pérdidas de las líneas con pérdida,
      escrita como número positivo.
    - Rango de descuento (`discount_band`): `0%` si no hubo descuento,
      `1%-5%` si fue mayor que 0 y hasta 5 %, `6%-10%` si fue mayor que 5 % y
      hasta 10 %, y `más de 10%` en otro caso.

    Genere tres archivos en `submission/`, sin el índice de Pandas y con las
    columnas en el orden indicado:

    1. `profitability_summary.csv`, con una sola fila: `lines` (cantidad de
       líneas), `orders` (pedidos distintos), `sales`, `profit`,
       `profit_margin`, `loss_lines` (cantidad de líneas con pérdida),
       `loss_line_rate` y `lost_profit`.

    2. `discount_summary.csv`, con una fila por rango de descuento, en el
       orden en que se definieron arriba: `discount_band`, `lines`, `sales`,
       `profit`, `profit_margin`, `loss_line_rate` y `lost_profit`.

    3. `priority_segments.csv`, con los cinco segmentos segmento–categoría
       que más utilidad pierden: `Customer Segment`, `Product Category`,
       `lines`, `sales`, `profit`, `profit_margin` y `lost_profit`. Considere
       solamente segmentos con al menos 100 líneas y ordénelos por
       `lost_profit` de mayor a menor.

    La función también debe retornar las tres tablas, en el mismo orden.

    Ejemplo del formato de `discount_summary.csv`:

        discount_band,lines,sales,profit,profit_margin,loss_line_rate,...
        0%,166,170539.05,29472.3789,0.1728,0.488,...
        ...
    """


    #data
    df = pd.read_csv("data/superstore_orders.csv.gz", sep=";", decimal=",")
    df["is_loss"] = df["Profit"] < 0
    df["loss"] = (-df["Profit"]).clip(lower=0)
    df["discount_band"] = pd.cut(
        df["Discount"],
        bins=[-1, 0, 0.05, 0.10, 10],
        labels=["0%", "1%-5%", "6%-10%", "más de 10%"],
    )


    #sss.........
    resumen = pd.DataFrame([{
        "lines": len(df),
        "orders": df["Order ID"].nunique(),
        "sales": df["Sales"].sum(),
        "profit": df["Profit"].sum(),
        "profit_margin": df["Profit"].sum() / df["Sales"].sum(),
        "loss_lines": int(df["is_loss"].sum()),
        "loss_line_rate": df["is_loss"].mean(),
        "lost_profit": df["loss"].sum(),
    }]) 

    #-.

    descuentos = df.groupby("discount_band", observed=False, as_index=False).agg(
        lines=("Order ID", "size"),
        sales=("Sales", "sum"),
        profit=("Profit", "sum"),
        loss_line_rate=("is_loss", "mean"),
        lost_profit=("loss", "sum"),)

    descuentos["profit_margin"] = descuentos["profit"] / descuentos["sales"]
    
    descuentos = descuentos[
        ["discount_band", "lines", "sales", "profit", "profit_margin", "loss_line_rate", "lost_profit"]]

    #-----

    segmentos = df.groupby(["Customer Segment", "Product Category"], as_index=False).agg(
        lines=("Order ID", "size"),
        sales=("Sales", "sum"),
        profit=("Profit", "sum"),
        lost_profit=("loss", "sum"),)

    #print(segmentos)
    
    segmentos = segmentos[segmentos["lines"] >= 100].sort_values("lost_profit", ascending=False).head(5)
    
    
    segmentos["profit_margin"] = segmentos["profit"] / segmentos["sales"]
    
    segmentos = segmentos[
        ["Customer Segment", "Product Category", "lines", "sales", "profit", "profit_margin", "lost_profit"]]

    #print(segmentos)

    carpeta_salida = Path("submission")
    carpeta_salida.mkdir(parents=True, exist_ok=True)
    resumen.to_csv(carpeta_salida / "profitability_summary.csv", index=False)
    descuentos.to_csv(carpeta_salida / "discount_summary.csv", index=False)
    segmentos.to_csv(carpeta_salida / "priority_segments.csv", index=False)

    return resumen, descuentos, segmentos
