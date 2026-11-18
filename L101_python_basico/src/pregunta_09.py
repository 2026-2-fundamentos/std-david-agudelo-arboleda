import csv
import gzip
from collections import Counter


def pregunta_09():
    """
    Cuente cuántas veces aparece cada clave en la quinta columna (`metrics`)
    de todo el archivo. Retorne un diccionario `{clave: cantidad}` con las
    claves en orden alfabético.

    Ejemplo del formato de la respuesta:

        {"aaa": 13, "bbb": 16, "ccc": 23, ...}
    """
    counts = Counter()
    with gzip.open("data/data.csv.gz", "rt", encoding="utf-8") as file:
        for row in csv.reader(file, delimiter="\t"):
            if row:
                for pair in row[4].split(","):
                    key, _ = pair.split(":")
                    counts[key] += 1
    return dict(sorted(counts.items()))
