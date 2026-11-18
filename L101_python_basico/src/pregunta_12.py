import csv
import gzip
from collections import defaultdict


def pregunta_12():
    """
    Para cada letra de la primera columna (`letter`), sume todos los valores
    numéricos de los pares `clave:valor` de la quinta columna (`metrics`).
    Retorne un diccionario `{letra: suma}` con las letras en orden alfabético.

    Ejemplo del formato de la respuesta:

        {"A": 177, "B": 187, "C": 114, ...}
    """
    totals = defaultdict(int)
    with gzip.open("data/data.csv.gz", "rt", encoding="utf-8") as file:
        for row in csv.reader(file, delimiter="\t"):
            if row:
                letter = row[0]
                for pair in row[4].split(","):
                    _, val = pair.split(":")
                    totals[letter] += int(val)
    return dict(sorted(totals.items()))
