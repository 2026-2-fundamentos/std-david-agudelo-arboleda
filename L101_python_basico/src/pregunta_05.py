import csv
import gzip
from collections import defaultdict


def pregunta_05():
    """
    Para cada letra de la primera columna (`letter`), encuentre el valor
    máximo y el valor mínimo de la segunda columna (`value`). Retorne una lista
    de tuplas `(letra, máximo, mínimo)` ordenada alfabéticamente por la letra.

    Ejemplo del formato de la respuesta:

        [("A", 9, 2), ("B", 9, 1), ...]
    """
    valores_por_letra = defaultdict(list)
    with gzip.open("data/data.csv.gz", "rt", encoding="utf-8") as archivo:
        for row in csv.reader(archivo, delimiter="\t"):
            if row:
                valores_por_letra[row[0]].append(int(row[1]))
    return [
        (letra, max(vals), min(vals))
        for letra, vals in sorted(valores_por_letra.items())
    ]
