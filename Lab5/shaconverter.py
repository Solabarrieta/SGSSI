import hashlib, sys, shutil

#Códigos de colores.
AMARILLO = '\033[93m'
ROJO = '\033[91m'
BLANCO = '\033[0m'

try:
	#Coge el archivo leyendo del argumento pasado.
	with open(sys.argv[1], 'rb') as f:
		bytes = f.read()
		#Calcula el resumen
		resumen=hashlib.sha256(bytes).hexdigest()
except Exception:
	print(ROJO + "No se ha podido encontrar el fichero\n" + BLANCO)

print(resumen)
	
exit(1)