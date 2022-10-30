import sys
import re
import hashlib
from operator import concat
from pickle import TRUE
import shutil
import secrets
import time


def getHeader(file):
    count = 0
    header = ""
    with open(file, 'r') as input:
        for line in input:
            if '\n' in line:
                count += 1
                header += line
            if count > 2:
                break
    return header


def validateNonce(file):
    valid = False
    pattern = re.compile("^[a-f0-9]{8} G[0-3][0-9]$")
    with open(file, "r") as input:
        for line in input:
            if bool(pattern.match(line)):
                valid = True
    return valid


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


def mineInAMinute(file):
    try:
        start_time = time.time()
        zeros = "0"
        while time.time() - start_time < 20:
            file = appendHex()
            digest = fileDigest(file)
            if digest.startswith(zeros):
                print("Prefijo: "+zeros)
                zeros += "0"
                copybigestzeros(file)
                digestWithZeros = fileDigest(file)
    except Exception as e:
        return e

    return digestWithZeros


def checkPoW(hashsum):
    powcheck = hashsum.startswith("00")
    return powcheck


try:

    header1 = getHeader(sys.argv[1])
    header2 = getHeader(sys.argv[2])
    equalHeaders = header1 == header2
    validNonce = validateNonce(sys.argv[2])
    hashsum = fileDigest(sys.argv[2])

    proof = checkPoW(hashsum)
    print("\n")
    print("###### Resultado ######")
    print('Cabeceras iguales: ', equalHeaders)
    print("Nonce valido: ", validNonce)
    #print('Digest: ', hashsum)
    print('Comienza por ceros: ', proof)
    print("El bloque es valido: ", equalHeaders and validNonce and proof)
    print("Digest del bloque minado: ", hashsum)
except Exception as e:
    print(e)
    exit(1)
