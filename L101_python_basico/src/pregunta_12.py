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
    totales = defaultdict(int)
    with gzip.open("data/data.csv.gz", "rt", encoding="utf-8") as archivo:
        for row in csv.reader(archivo, delimiter="\t"):
            if row:
                letra = row[0]
                for par in row[4].split(","):
                    _, val = par.split(":")
                    totales[letra] += int(val)
    return dict(sorted(totales.items()))
