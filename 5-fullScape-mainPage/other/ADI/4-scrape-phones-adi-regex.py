# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoAlertPresentException
import unittest, time, re
import tldextract

def url_check(url):
	if "http" in url:
		url = url
	else:
		url = 'http://' + url
	return url



inputfile = open("input_scrape_phones.txt")
urls = [url.strip() for url in inputfile.readlines()]

driver = webdriver.Chrome()
#driver.set_window_size(1024, 768) # set the window size that you need 
file = open("output/output_phone_scrape.csv", "w")

for url in urls:

	print("Processing: " + url)
	url = url_check(url)
	driver.get(url)
	content = driver.find_element_by_tag_name("body")
	phones = re.findall(r'(\d\d\d-\d\d\d-\d\d\d\d)', content.text)

	if not phones:
		print("No numbers")
	else:
		file.write(url + ",Unpaid2," + phones[0] + ",")
		for phone in phones:
			print(url + " Unpaid: " + phone)



	driver.get(url + "?provider=google")
	content = driver.find_element_by_tag_name("body")
	phones = re.findall(r"(\d\d\d-\d\d\d-\d\d\d\d)", content.text)
	if len(phones) == 0:
		print("No numbers")
	else:
		file.write("Paid," + phones[0] + "\n")
		for phone in phones:
			print(url + " Paid: " + phone)


file.close
driver.quit()
