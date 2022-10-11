import hashlib
from pickle import TRUE
import sys
import shutil
import secrets
import os


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


try:
    file = appendHex()
    digest = fileDigest(file)
    while TRUE:
        os.remove(file)
        file = appendHex()
        digest = fileDigest(file)
        if digest[0] == "0":
            break
    print(digest)

except Exception:
    print("No se ha podido encontrar el fichero\n")
    exit(1)
