import csv
import gzip
from collections import defaultdict


def pregunta_11():
    """
    La cuarta columna (`codes`) contiene letras minúsculas separadas por
    comas. Para cada una de esas letras, sume los valores de la segunda
    columna (`value`) de los registros en los que aparece. Retorne un
    diccionario `{letra: suma}` con las letras en orden alfabético.

    Ejemplo del formato de la respuesta:

        {"a": 122, "b": 49, "c": 91, ...}
    """
    totales = defaultdict(int)
    with gzip.open("data/data.csv.gz", "rt", encoding="utf-8") as archivo:
        for row in csv.reader(archivo, delimiter="\t"):
            if row:
                val = int(row[1])
                for code in row[3].split(","):
                    totales[code] += val
    return dict(sorted(totales.items()))
