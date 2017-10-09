import os
import re
import shutil
import tarfile

import constants

def list_tree(dir_path, extensions=["*"]):
	list_paths = []
	for name in os.listdir(dir_path):		
		full_path = os.path.join(dir_path, name)	
		for ext in extensions:
			if re.search (r".*\." + ext, full_path, re.IGNORECASE):                        
				list_paths.append(full_path)
			if os.path.isdir(full_path) and name != ".svn":
				list_paths.append(list_tree(full_path))
	return list_paths

def clear(dir_path):
	list_paths = list_tree(dir_path)
	for path in list_paths:
		file_name = os.path.basename(path)
		if file_name.find("-") > -1:
			file_name_new = file_name.replace("-", "")
			shutil.move(path, os.path.join(os.path.dirname(path), file_name_new))

def move(src_path, dst_path):
	file_name = os.path.basename(src_path)
	shutil.move(src_path, os.path.join(dst_path, file_name))

def get_properties_file_book(book, log):
	try:
		book.size = os.stat(os.path.join(constants.INPUT_PATH, book.filename)).st_size
	except Exception, e:
		log.write("faild to read %s: %s\n" % (book.filename, e))
	book.filetype = book.filename[book.filename.rfind(".") + 1:].upper()
	return book

def backup_db():
	if os.path.exists(constants.BACK_DB):
		os.remove(constants.BACK_DB)
	shutil.copy(constants.DB_PATH, constants.BACK_DB)

def compress(file_path, file_name):
	tar = tarfile.open(os.path.join(file_path, "%s.tar.bz2" % file_name), "w:bz2")
	tar.add(os.path.join(file_path,file_name), arcname=file_name)
	tar.close()
	os.remove(os.path.join(file_path, file_name))

def uncompress(file_path, file_name):
	tar = tarfile.open(os.path.join(file_path, file_name), "r:bz2")
	tar.extract(file_name[:-8], file_path)
	tar.close()
	if (os.path.exists(os.path.join(file_path, file_name[:-8]))):
		os.remove(os.path.join(file_path, file_name))

if __name__ == "__main__":
	backup_db()
	#compress("D:\\work\\django\\library_usb\\files", "007222438X Hacking_Exposed_Web_Applications.pdf")
	#uncompress("D:\\work\\django\\library_usb\\files", "007222438X Hacking_Exposed_Web_Applications.pdf.tar.bz2")

