import csv
import gzip
from collections import defaultdict


def pregunta_08():
    """
    Repita la pregunta 7, pero ahora cada lista de letras debe contener cada
    letra una sola vez y estar ordenada alfabéticamente. Retorne una lista de
    tuplas `(valor, letras)` ordenada por el valor.

    Ejemplo del formato de la respuesta:

        [(0, ["C"]), (1, ["B", "E"]), (2, ["A", "E"]), ...]
    """
    letters_by_value = defaultdict(set)
    with gzip.open("data/data.csv.gz", "rt", encoding="utf-8") as file:
        for row in csv.reader(file, delimiter="\t"):
            if row:
                letters_by_value[int(row[1])].add(row[0])
    return [
        (val, sorted(letters))
        for val, letters in sorted(letters_by_value.items())
    ]
