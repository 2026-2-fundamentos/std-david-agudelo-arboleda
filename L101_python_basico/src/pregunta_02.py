import csv
import gzip
from collections import Counter


def pregunta_02():
    """
    Cuente cuántos registros hay para cada letra de la primera columna
    (`letter`). Retorne una lista de tuplas `(letra, cantidad)` ordenada
    alfabéticamente por la letra.

    Ejemplo del formato de la respuesta:

        [("A", 8), ("B", 7), ("C", 5), ...]
    """
    counts = Counter()
    with gzip.open("data/data.csv.gz", "rt", encoding="utf-8") as file:
        for row in csv.reader(file, delimiter="\t"):
            if row:
                counts[row[0]] += 1
    return sorted(counts.items())
