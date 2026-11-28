import re
import pandas as pd


def pregunta_01():
    """
    El archivo `data/clusters_report.txt` es un reporte de clústeres de
    palabras clave pensado para ser leído por una persona, no por un programa:
    los encabezados ocupan varias líneas, las columnas están alineadas con
    espacios y la lista de palabras clave de un clúster continúa en las líneas
    siguientes.

    Su tarea es convertir ese reporte en un DataFrame de Pandas con una fila
    por clúster y las columnas:

    - `cluster`: número del clúster, como entero.
    - `cantidad_de_palabras_clave`: como entero.
    - `porcentaje_de_palabras_clave`: como número decimal; por ejemplo, el
      texto `15,9 %` debe quedar como `15.9`.
    - `principales_palabras_clave`: todas las palabras clave del clúster en un
      solo texto, separadas por una coma y un único espacio.

    Retorne el DataFrame.

    Ejemplo del formato de la respuesta (se omite la última columna):

           cluster  cantidad_de_palabras_clave  porcentaje_de_palabras_clave
        0        1                         105                          15.9
        1        2                         102                          15.4
        ...
    """
    patron = re.compile(r"^\s*(\d+)\s+(\d+)\s+([\d,]+)\s*%\s+(.*)$")
    filas = []
    actual = None

    with open("data/clusters_report.txt", encoding="utf-8") as archivo:
        for linea in archivo.readlines()[4:]:
            match = patron.match(linea)
            if match:
                if actual is not None:
                    filas.append(actual)
                actual = {
                    "cluster": int(match.group(1)),
                    "cantidad_de_palabras_clave": int(match.group(2)),
                    "porcentaje_de_palabras_clave": float(
                        match.group(3).replace(",", ".")
                    ),
                    "principales_palabras_clave": match.group(4).strip(),
                }
            elif actual is not None and linea.strip():
                actual["principales_palabras_clave"] += " " + linea.strip()

    if actual is not None:
        filas.append(actual)

    for row in filas:
        row["principales_palabras_clave"] = " ".join(
            row["principales_palabras_clave"].split()
        ).rstrip(".")

    return pd.DataFrame(filas)
