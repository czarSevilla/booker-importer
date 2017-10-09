from mysql_connector import MySQLConnector
from constants import *

class MySQLDao():
	def __init__(self, log):
		self.connector = MySQLConnector()
		self.log = log
		

	def __str__(self):
		return "dao"

	def book_exists(self, isbn):
		row = self.connector.execute_bind_result_set("select id from book where isbn10 = %s or isbn13 = %s", (isbn, isbn))		
		return row != None and len(row) > 0 and row[0][0] != None

	def saveAuthor(self, name):
		row = self.connector.execute_bind_result_set("select id from author where lower(name) = %s", (name.lower(),))
		if row == None or len(row) == 0:
			try:
				self.connector.execute_bind_query("insert into author(name, date_created, last_updated, total, version) values(%s, now(), now(), 1, 0)", (name,))
			except Exception, e:
				msg = "Error al insertar author %s: %s" % (name, e)
				self.log.write(msg)
			row_id = self.connector.execute_bind_result_set("select id from author where lower(name) = %s", (name.lower(),))
			id = row_id[0][0]
			if id == None:
				return 0
			else:				
				return id
		else:
			self.connector.execute_bind_query("update author set version = version + 1, total = total + 1 where lower(name) = %s", (name.lower(),))
			return row[0][0]		
	
	def savePublisher(self, name):
		row = self.connector.execute_bind_result_set("select id from publisher where lower(name) = %s", (name.lower(),))
		if row == None or len(row) == 0:
			self.connector.execute_bind_query("insert into publisher(name, date_created, last_updated, total, version) values(%s, now(), now(), 1, 0)", (name,))
			row_id = self.connector.execute_bind_result_set("select id from publisher where lower(name) = %s", (name.lower(),))			
			if row_id == None or len(row_id) == 0:
				print "Error al publisher author: " + name
				return 0
			else:				
				return row_id[0][0]
		else:
			self.connector.execute_bind_query("update publisher set version = version + 1, total = total + 1 where lower(name) = %s", (name.lower(),))
			return row[0][0]	
	
	def save(self, book):		
		publisher_id = self.savePublisher(book.publisher)
		for author in book.authors:
			book.authors_id.append(self.saveAuthor(author))		
			if len(book.isbn10) > 10:
				book.isbn10 = book.isbn10[0:10]
		sql = "insert into book(title, isbn10, isbn13, publisher_id, pages, date_publication, image, file_size, file_type, path, date_created, last_updated, version, deprecated) values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, now(), now(), 0, %s)"
		self.connector.execute_bind_query(sql, (book.title, book.isbn10, book.isbn13, publisher_id, book.pages, book.pub_date, book.image, book.size, book.filetype, book.filename, False))
		book_id = self.connector.execute_result_set("select last_insert_id()")
		if book_id == None or len(book_id) == 0:
			return False
		sql = "insert into book_authors(author_id, book_id) values(%s, %s)"
		for author_id in book.authors_id:
			try:
				self.connector.execute_bind_query(sql, (author_id, book_id[0][0]))
			except Exception, ie:
				msg = "Error al insertar relacion author libro (%s, %s): %s" % (author_id, book_id[0][0], ie)
				self.log.write(msg)
		return True
	
	def count_new_books(self, import_time):
		rs = self.connector.execute_bind_result_set("select count(*) from book where date_format(date_created, '%%Y%%m%%d%%H%%i%%s') >= %s", (import_time,))
		if len(rs) > 0:
			return rs[0][0]
		return 0
		
	
	def finalize(self):
		self.connector.finalize()
