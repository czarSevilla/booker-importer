import MySQLdb
from connector import Connector

class MySQLConnector(Connector):
	def __init__ (self, host="localhost", user="reader", passwd="reader", db="books_library"):
		self.conn = MySQLdb.connect(host=host, user=user, passwd=passwd, db=db, charset="utf8", init_command="set names utf8")
		self.cursor = self.conn.cursor()
