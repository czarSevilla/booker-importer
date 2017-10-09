#!/usr/bin/python
import os, sys, shutil

def sincronizar(origen, destino):
	msg = "sincronizando de %s a %s" % (origen, destino)
	print(msg)
	for filename in os.listdir(origen):
		if (not os.path.exists(os.path.join(destino, filename)) and filename != ".svn"):
			msg = "copiando archivo: %s " % filename
			print(msg)
			shutil.copy(os.path.join(origen, filename), os.path.join(destino, filename))

def sincronizar_app(origen, destino):
	thumbs_origen = os.path.join(origen, "publications", "media", "images", "thumbs")
	thumbs_destino = os.path.join(destino, "publications", "media", "images", "thumbs")
	files_origen = os.path.join(origen, "files")
	files_destino = os.path.join(destino, "files")
	db_origen = os.path.join(origen, "publications", "publications.sqlite3")
	db_destino = os.path.join(destino, "publications", "publications.sqlite3")
	if (not os.path.exists(files_origen)):
		print("No se encuentra la carpeta \"files\" origen")
		exit()
	if (not os.path.exists(files_destino)):
		print("No se encuentra la carpeta \"files\" destino")
		exit()
	sincronizar(files_origen, files_destino)
	if (not os.path.exists(thumbs_origen)):
		print("No se encuentra la carpeta \"thumbs\" origen")
		exit()
	if (not os.path.exists(thumbs_destino)):
		print("No se encuentra la carpeta \"thumbs\" destino")
		exit()
	sincronizar(thumbs_origen, thumbs_destino)
	if (not os.path.exists(db_origen)):
		print("No se encuentra la base de datos origen")
		exit()
	print("sincronizando base de datos")
	if (os.path.exists(db_destino)):
		shutil.rmtree(db_destino, True)
	shutil.copy(db_origen, db_destino)

		

if __name__ == "__main__":
	if (len(sys.argv) < 3):
		print("El uso correcto es:  \nsincronizar.py ruta_origen ruta_destino")
		exit()
	if (len(sys.argv) == 3):
		if (not os.path.exists(sys.argv[1])):
			print("No se encuentra la ruta de origen")
			exit()
		if (not os.path.exists(sys.argv[2])):
			print("No se encuentra la ruta de destino")
			exit()
		sincronizar(sys.argv[1], sys.argv[2])
	if (len(sys.argv) == 4):
		if (sys.argv[1] != "app"):
			print("El uso correcto es: sincronizar.py app ruta_app_origen ruta_app_destino")
			exit()
		if (not os.path.exists(sys.argv[2])):
			print("No se encuentra la ruta de origen")
			exit()
		if (not os.path.exists(sys.argv[3])):
			print("No se encuentra la ruta de destino")
			exit()
		sincronizar_app(sys.argv[2], sys.argv[3])
