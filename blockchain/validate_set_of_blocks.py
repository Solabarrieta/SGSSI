import sys
import re
import hashlib
from operator import concat
from pickle import TRUE
import shutil
import secrets
import time
import os


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
        while time.time() - start_time < 60:
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


def isBlockValid(originalFile, minedFile):
    header1 = getHeader(originalFile)
    header2 = getHeader(minedFile)
    equalHeaders = header1 == header2
    validNonce = validateNonce(minedFile)
    hashsum = fileDigest(minedFile)
    proof = checkPoW(hashsum)
    isValid = equalHeaders and validNonce and proof
    return isValid, hashsum, equalHeaders, validNonce, proof


def countZeros(hashsum):
    count = 0
    for index in range(len(hashsum)):
        if hashsum[index] == "0":
            count += 1
        if hashsum[index] != "0":
            break
    return count


try:
    files = os.listdir(sys.argv[2])
    bigestZeros = 0
    auxCount = 0
    for path in files:
        fichero = path
        block = r"{0}{1}".format(sys.argv[2], fichero)
        isValid, digest, _, _, _ = isBlockValid(sys.argv[1], block)
        if isValid:
            auxCount = countZeros(digest)
            if auxCount > bigestZeros:
                bigestZeros = auxCount
                bigestZerosDigest = digest
                bloqueCandidato = block
    print("########### RESULTADO ###########")
    print("Bloque con m??s ceros: ", bigestZerosDigest)
    print("Cantidad de ceros", bigestZeros)
    print("Nombre del bloque candidato: ", bloqueCandidato)
except Exception as e:
    exc_type, exc_obj, exc_tb = sys.exc_info()
    fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
    print(exc_type, fname, exc_tb.tb_lineno, e)
    exit(1)
