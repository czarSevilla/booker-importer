from constants import *
from file_utils import *
from sqlite3_connector import *

import os
import sys

def check_files():
	print("Comparando archivos...")
	files = list_tree(os.path.join("..", CLEAN_PATH))
	conn = SQLite3Connector(db=os.path.join("..", DB_PATH))
	conn.execute_query("drop table if exists files");
	conn.execute_query("create table files(name varchar(256))")
	for file_name in files:
		conn.execute_bind_query("insert into files(name) values(?)", (os.path.basename(file_name),))
	rs1 = conn.execute_result_set("select path from books where path not in (select name from files)")
	if len(rs1) > 0:
		print("Los siguientes archivos no se encuentran en el sistema de archivos: \n")
		for row in rs1:
			print("%s\n" % row[0])
	rs2 = conn.execute_result_set("select name from files where name not in (select path from books)")
	if len(rs2) > 0:
		print("Los siguientes archivos no se encuentran en la base de datos: \n")
		for row in rs2:
			print("%s\n" % row[0])
	conn.finalize()
	print("Termina comparacion de archivos")

def check_images():
	print("Comparando imagenes...")
	files = list_tree(os.path.join("..", THUMBAILS_PATH))
	conn = SQLite3Connector(db=os.path.join("..", DB_PATH))
	conn.execute_query("drop table if exists files")
	conn.execute_query("create table files(name varchar(256))")
	for file_name in files:
		conn.execute_bind_query("insert into files(name) values(?)", (os.path.basename(file_name),))
	rs1 = conn.execute_result_set("select image, isbn10, isbn13, title from books where image not in (select name from files)")
	if len(rs1) > 0:
		print("Las siguientes imagenes no se encuentran en el sistema de archivos: \n")
		for row in rs1:
			print("%s\t%s\t%s\t%s\n" % (row[0], row[1], row[2], row[3]))
	rs2 = conn.execute_result_set("select name from files where name not in (select image from books)")
	if len(rs2) > 0:
		print("Las siguientes imagenes no se encuentran en la base de datos: \n")
		for row in rs2:
			print("%s\n" % row[0])
	conn.finalize()
	print("Termina comparacion de imagenes")

def import_default_tags():
	tags = ["AGILE", "AJAX", "ALGORITHMS", "ANALYSIS", "BUSINESS", "C++", "CERTIFICATION", "CSS", "DATABASE", 
"DESIGN", "DJANGO", "ENGINEERING", "FRAMEWORK", "GRAILS", "GROOVY", "J2EE", "JAVA", "JAVASCRIPT", "LINUX", 
"MANAGEMENT", "MATHEMATICS", "MICROSOFT", "MOBILE", "MYSQL", "ORACLE", "PATTERNS", "PHP", "PYTHON", 
"RUBY", "SECURITY", "SPRING", "TESTING", "UBUNTU", "UML", "UNIX", "WEB", "XML"]

	print("Revisando si hay tags...")
	conn = SQLite3Connector(db=os.path.join("..", DB_PATH))
	rs = conn.execute_result_set("select count(*) from tags")
	if rs and len(rs) > 0:
		total = rs[0][0]
		if total > 0:
			print("Ya hay tags")
		else:
			print("No se encontraron tags")
			print("Se comienza importacion de tags")
			for tag in tags:
				conn.execute_bind_query("insert into tags(name, total, created_at, updated_at) values(?, 0, datetime(), datetime())", (tag, ))
	conn.finalize()
	print("Termina inicializacion de tags")

def initialize_tags_relations():
	print("Generando relaciones con tags...")
	conn = SQLite3Connector(db=os.path.join("..", DB_PATH))
	rs = conn.execute_result_set("select count(*) from books_tags")
	if rs and len(rs) > 0:
		total = rs[0][0]
		if total > 0:
			print("Ya hay relaciones entre books y tags")
		else:
			print("No se encontraron relaciones entre books y tags")
			print("Se comienza relacion de books y tags")
			rs1 = conn.execute_result_set("select id, name from tags")
			for row in rs1:
				rs2 = conn.execute_bind_result_set("select id from books where upper(title) like ?", ("%" + row[1] + "%", ))
				for row1 in rs2:
					conn.execute_bind_query("insert into books_tags(book_id, tag_id) values(?, ?)", (row1[0], row[0]))
				conn.execute_bind_query("update tags set total = total + ? where id = ?", (len(rs2), row[0]))
	conn.finalize()
	print("Termina inicializacion de tags")


if __name__ == "__main__":
	opc = int(sys.argv[1])
	if opc == 1:
		check_files()
	if opc == 2:
		check_images()
	if opc == 3:
		check_files()
		check_images()
	if opc == 4:
		import_default_tags()
	if opc == 5:
		initialize_tags_relations()