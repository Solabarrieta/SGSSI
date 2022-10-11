import hashlib
from pickle import TRUE
import sys
import shutil
import secrets
import os

# Códigos de colores.
AMARILLO = '\033[93m'
ROJO = '\033[91m'
BLANCO = '\033[0m'


def fileDigest(file):
    with open(file, 'rb') as f:
        bytes = f.read()
        # Calcula el resumen
        resumen = hashlib.sha256(bytes).hexdigest()
    return resumen


def appendHex():
    hex = secrets.token_hex(4)
    original = r"{}".format(sys.argv[1])
    copia = r"{}SHA.txt".format(sys.argv[1][:-4])
    shutil.copyfile(original, copia)
    with open("{}SHA.txt".format(sys.argv[1][:-4]), 'a') as f:
        # Guarda el documento con la línea adicional.
        f.write("{}".format(hex))
        f.write(" ")
        f.write("G01")
    return copia



try:
    # Coge el archivo leyendo del argumento pasado.

    # Crear copia del archivo
    file = appendHex()
    digest = fileDigest(file)
    while TRUE:
        os.remove(file)
        file = appendHex()
        digest = fileDigest(file)
        if digest [0] == "0":
            break
    print(digest)

except Exception:
    print(ROJO + "No se ha podido encontrar el fichero\n" + BLANCO)
    exit(1)
