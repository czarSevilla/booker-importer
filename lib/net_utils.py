#!/usr/bin/python

import base64, hashlib, hmac, time
import urllib
import os
import sys
from urllib import urlencode, quote_plus
from xml.dom import minidom
from book import Book
from constants import *

def get_amazon_signed_url(isbn):
    AWS_ACCESS_KEY_ID = "AKIAJQBK4RQVNVCFOWVA"
    AWS_SECRET_ACCESS_KEY = "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"
    base_url = "http://ecs.amazonaws.com/onca/xml"
    url_params = dict(
        Service='AWSECommerceService', 
        Operation='ItemLookup', 
        IdType='ISBN', 
        ItemId=isbn,
        SearchIndex='Books',
        AWSAccessKeyId=AWS_ACCESS_KEY_ID,  
        ResponseGroup='Images,ItemAttributes')
    #Can add Version='2009-01-06'. What is it BTW? API version?
    # Add a ISO 8601 compliant timestamp (in GMT)
    url_params['Timestamp'] = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    # Sort the URL parameters by key
    keys = url_params.keys()
    keys.sort()
    # Get the values in the same order of the sorted keys
    values = map(url_params.get, keys)
    # Reconstruct the URL parameters and encode them
    url_string = urlencode(zip(keys,values))
    #Construct the string to sign
    string_to_sign = "GET\necs.amazonaws.com\n/onca/xml\n%s" % url_string
    # Sign the request
    signature = hmac.new(
        key=AWS_SECRET_ACCESS_KEY,
        msg=string_to_sign,
        digestmod=hashlib.sha256).digest()
    # Base64 encode the signature
    signature = base64.encodestring(signature).strip()
    # Make the signature URL safe
    urlencoded_signature = quote_plus(signature)
    url_string += "&Signature=%s" % urlencoded_signature	
    return "%s?%s" % (base_url, url_string)

def get_book(isbn, log):
	book = get_amazon_book(isbn, log)
	return book

def get_amazon_book(isbn, log):
	try:
		url = get_amazon_signed_url(isbn)
		response = urllib.urlopen(url)
		html = response.read()
	except IOError, e:
		log.write("%s: %s\n" % (isbn, e))
		return None
	xml = minidom.parseString(html)
	#validar el request	
	valid_node_list = xml.getElementsByTagName("IsValid")
	if len(valid_node_list) == 0:
		log.write("No se encontro el elemento IsValid para %s\n" % isbn)
		return None
	is_valid = valid_node_list[0].childNodes[0].data == "True"
	if is_valid:		
		error_node_list = xml.getElementsByTagName("Error")		
		if len(error_node_list) > 0:
			error_message = error_node_list[0].getElementsByTagName("Message")[0].childNodes[0].data		
			log.write("ocurrio un error: %s\n" % error_message)
			return None
		else:
			item_node_list = xml.getElementsByTagName("Item")
			if len(item_node_list) > 0:
				item_book = item_node_list[0]
				book = Book()
				#elementos indispensables que causarian un error el no tenerlos
				try:
					book.title = item_book.getElementsByTagName("Title")[0].childNodes[0].data
					book.publisher = item_book.getElementsByTagName("Publisher")[0].childNodes[0].data
					authors = item_book.getElementsByTagName("Author")					
					if len(authors) == 0:
						creators = item_book.getElementsByTagName("Creator")
						if len(creators) == 0:
							raise Exception("Se requiere de uno o mas autores")
						else:
							for creator in creators:
								author_data = creator.childNodes[0].data
								if author_data not in book.authors:
									book.authors.append(author_data)
					for author_item in authors:
						author_data = author_item.childNodes[0].data
						if author_data not in book.authors:
							book.authors.append(author_data)
					book.isbn10 = item_book.getElementsByTagName("ISBN")[0].childNodes[0].data
				except Exception, e:
					log.write ("No se cumplen los requerimientos minimos: %s\n" % e)
					return None
				#elementos opcionales
				if len(item_book.getElementsByTagName("EAN")) > 0:
					book.isbn13 = item_book.getElementsByTagName("EAN")[0].childNodes[0].data
				if len(item_book.getElementsByTagName("NumberOfPages")) > 0:
					book.pages = item_book.getElementsByTagName("NumberOfPages")[0].childNodes[0].data
				if len(item_book.getElementsByTagName("PublicationDate")) > 0:
					pub_date = item_book.getElementsByTagName("PublicationDate")[0].childNodes[0].data
					if len(pub_date) == 4:
						pub_date = pub_date + "-07-15"
					if len(pub_date) == 7:
						pub_date = pub_date + "-15" 
					book.pub_date = pub_date
				if len(item_book.getElementsByTagName("MediumImage")) > 0:
					image_node = item_book.getElementsByTagName("MediumImage")[0]
					if len(image_node.getElementsByTagName("URL")) > 0:
						book.small_image_url = image_node.getElementsByTagName("URL")[0].childNodes[0].data
						book.image = get_image(os.path.join(THUMBAILS_PATH, book.isbn10 + ".jpg"), book.small_image_url, log)				
				return book
			else:
				log.write("sin elemento item")
				return None
	return None


def get_image(path, url, log):
	if not os.path.exists(path):
		try:
			urllib.urlretrieve(url, path)
			return os.path.basename(path)
		except Exception, e:
			log.write("Error al obtener la imagen %s: %s\n" % (path, e))
			return ""
	else:
		return os.path.basename(path)

if __name__ == "__main__":
	print get_amazon_signed_url(sys.argv[1])
