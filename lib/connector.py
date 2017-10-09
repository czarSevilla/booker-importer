class Connector:
	def execute_bind_result_set(self, query, bind):
		self.cursor.execute(query, bind)
		result_set = self.cursor.fetchall()
		return result_set

	def execute_result_set (self, query):
		self.cursor.execute(query)
		result_set = self.cursor.fetchall()
		return result_set
	
	def execute_query (self, query):
		self.cursor.execute(query)
		self.conn.commit()

	def execute_bind_query (self, query, bind):
		self.cursor.execute(query, bind)
		self.conn.commit()
	
	def finalize(self):
		self.cursor.close()
		self.conn.close()