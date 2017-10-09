from threading import Thread
from net_utils import *
from file_utils import *
import os
from mysql_dao import MySQLDao

class BookDownloaderThread(Thread):
	def __init__(self, index, log, lock):
		Thread.__init__(self)
		self.isbns = {}
		self.log = log
		self.index = index
		self.lock = lock
	
	def addISBN(self, isbn, path):
		self.isbns[isbn] = path

	def run(self):
		dao = MySQLDao(self.log)
		for isbn in self.isbns:
			book = get_book(isbn, self.log)			
			if book != None:
				try:
					print("%s: download %s\b" % (self.index, book))
				except UnicodeEncodeError, e:
					self.log.write("%s: %s\n" % (isbn, e))
				book.filename = os.path.basename(self.isbns[isbn])
				book = get_properties_file_book(book, self.log)
				success_on_save = False
				self.lock.acquire()
				try:
					success_on_save = dao.save(book)
				except UnicodeEncodeError, ex:
					self.log.write("%s\n" % ex)
					success_on_save = False
				self.lock.release()
				if success_on_save:
					move(self.isbns[isbn], CLEAN_PATH)
				else:
					msg = "Book fails to save %s\n" % os.path.basename(self.isbns[isbn])
					print(msg)
					self.log.write(msg)
					move(self.isbns[isbn], ERROR_PATH)
			else:
				msg = "Book not found: %s\n" % os.path.basename(self.isbns[isbn])
				print(msg)
				self.log.write(msg)
				move(self.isbns[isbn], ERROR_PATH)

		dao.finalize()
