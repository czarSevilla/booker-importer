import sqlite3
from connector import Connector

class SQLite3Connector(Connector):
	def __init__ (self, db="../db/development.sqlite3"):
		self.conn = sqlite3.connect(db)
		self.cursor = self.conn.cursor()
