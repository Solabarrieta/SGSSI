import hashlib
from operator import concat
from pickle import TRUE
import sys
import shutil
import secrets
import os
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
        f.write(" ")
        f.write("G01")
    return copia


def copybigestzeros(file):
    original = r"{}".format(file)
    copia = r"{}ZEROS.txt".format(sys.argv[1][:-4])
    shutil.copyfile(original, copia)


try:
    start_time = time.time()
    file = appendHex()
    digest = fileDigest(file)
    copybigestzeros(file)
    zeros = "0"
    while time.time() - start_time < 60:
        os.remove(file)
        file = appendHex()
        digest = fileDigest(file)
        if digest.startswith(zeros):
            zeros += "0"
            print(zeros)
            print(digest)
            copybigestzeros(file)
    print(digest)
    print(zeros)
except Exception:
    print(ROJO + "No se ha podido encontrar el fichero\n" + BLANCO)
    exit(1)
