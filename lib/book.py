class Book:
	def __init__(self):
		self.isbn13 = ""
		self.isbn10 = ""
		self.title = ""
		self.long_title = ""
		self.publisher = ""
		self.publisher_external_id = ""
		self.pub_date = ""
		self.authors = []
		self.filename = ""
		self.image = ""
		self.publisher_id = 0
		self.authors_id = []
		self.size = 0
		self.filetype = ""
		self.small_image_url = ""
		self.large_image_url = ""
		self.fuente = ""
		self.author = ""
		self.pages = 0
	
	def __str__(self):
		return self.title
