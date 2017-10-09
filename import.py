#!/usr/bin/python

from lib.mysql_dao import MySQLDao
from lib.book import Book
from lib.file_utils import *
from lib.threads import *
from lib.constants import *

import time
import os
import re
import threading

def import_books():	
	log = open(LOG_FILE, "w")
	dao = MySQLDao(log)
	import_ini = time.gmtime()
	log.write("start book import at: %s\n" % time.strftime("%Y%m%d %H:%M:%S", import_ini))
	time_ini = time.clock()
	msg = "clean INPUT"
	print(msg)
	log.write(msg + "\n")
	clear(INPUT_PATH)
	msg = "set up threads"
	paths = list_tree(INPUT_PATH, EXTS)
	books_to_download = {}
	for path in paths:		
		file_name = os.path.basename(path)		
		isbn_match = re.match(r"(?P<isbn>\A[\w]{13}|\A[\w]{10}) ", file_name)
		if isbn_match:
			isbn = isbn_match.group("isbn")
			if not dao.book_exists(isbn):			
				books_to_download[isbn] = path
			else:
				msg = "book exists: %s\n" % file_name
				print msg
				log.write(msg)
				move(path, DUPLICATE_PATH)
		else:
			msg = "invalid isbn: %s\n" % file_name
			print msg
			log.write(msg)
			move(path, ERROR_PATH)
	total_books = len(books_to_download)
	downloaders = []
	lock = threading.Lock()
	for i in range(0, min(total_books, TOTAL_THREADS)):
		downloaders.append(BookDownloaderThread(i + 1, log, lock))	
	index = 0
	for isbn in books_to_download:
		downloaders[index].addISBN(isbn, books_to_download[isbn])
		index = index + 1 if index < len(downloaders) - 1 else 0
	msg = "start threads"
	print(msg)
	log.write(msg + "\n")
	for downloader in downloaders:
		downloader.start()
	for downloader in downloaders:
		downloader.join()
	log.write("end book import at: %s\n" % time.strftime("%Y%m%d %H:%M:%S", time.gmtime()))
	new_books = dao.count_new_books(time.strftime("%Y%m%d%H%M%S", import_ini))
	log.write("%s of %s books successful imported!\n" % (new_books, total_books))
	time_end = time.clock()
	log.write("import process in %s seconds:" % (time_end - time_ini))
	dao.finalize()
	log.close()


if __name__ == "__main__":
	import_books()