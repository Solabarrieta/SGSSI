import hashlib
from operator import concat
from pickle import TRUE
import sys
import shutil
import secrets
import time


def fileDigest(file):
    with open(file, 'rb') as f:
        bytes = f.read()
        resumen = hashlib.sha256(bytes).hexdigest()
    return resumen


def appendHex():
    hex = secrets.token_hex(4)
    original = r"{}".format(sys.argv[1])
    copia = r"{}SHA.txt".format(sys.argv[1][:-4])
    shutil.copyfile(original, copia)
    with open("{}SHA.txt".format(sys.argv[1][:-4]), 'a') as f:
        f.write("{}".format(hex))
    return copia


def copybigestzeros(file):
    original = r"{}".format(file)
    copia = r"{}ZEROS.txt".format(sys.argv[1][:-4])
    shutil.copyfile(original, copia)


try:
    start_time = time.time()
    zeros = "0"
    while time.time() - start_time < 60:
        file = appendHex()
        digest = fileDigest(file)
        if digest.startswith(zeros):
            print("Prefijo: "+zeros)
            zeros += "0"
            copybigestzeros(file)
            digestWithZeros = fileDigest(file)
    print("Longitud del prefijo: ", len(zeros[:-1]))
    print(digestWithZeros)
except Exception:
    print("No se ha podido encontrar el fichero\n")
    exit(1)
