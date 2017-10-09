#!/usr/bin/python

import smtplib
import urllib2
import re
import os

file_name = ".my_ip"

def send_mail(msg):
	server = smtplib.SMTP('smtp.gmail.com')
	server.starttls()
	server.login("czar.sevilla", "princesitasam")
	server.sendmail("czar.sevilla@gmail.com", "czar.sevilla@gmail.com", msg)
	server.quit()
	
def get_current_ip():
	req = urllib2.urlopen("http://www.ipchicken.com")
	html = req.read()
	req.close()
	m = re.search('\d{3}\.\d{3}\.\d{3}\.\d{3}', html)
	ip = m.group(0)
	return ip
	
def get_last_ip():
	if (os.path.exists(file_name)):
		f = file(file_name, "r")
		ip = f.read()
		f.close()
		return ip
	return ""
	
def save_ip(ip):
	f = file(file_name, "w")
	f.write(ip)
	f.close()
	

if __name__ == "__main__":
	current_ip = get_current_ip()
	last_ip = get_last_ip()
	if (current_ip == last_ip):
		print("nothing to do")
	else:
		print("current_ip: %s" % current_ip)
		save_ip(current_ip)
		send_mail(current_ip)
	
