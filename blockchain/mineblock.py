import hashlib
from operator import concat
from pickle import TRUE
import sys
import shutil
import secrets
import time
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
        f.write("Ge59")
    return copia


def copybigestzeros(file):
    original = r"{}".format(file)
    copia = r"./minedblocks{}.e59.txt".format(sys.argv[1][:-4][7:])
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
    os.remove(file)
except Exception as e:
    print('Error: ', e)
    exit(1)
