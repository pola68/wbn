# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoAlertPresentException
import unittest, time, re
import tldextract

#depot = DepotManager.get()

inputfile = open("input_scrape_phones.txt")
urls = [url.strip() for url in inputfile.readlines()]

driver = webdriver.Chrome()
#driver.set_window_size(1024, 768) # set the window size that you need 
file = open("output/output_phone_scrape.csv", "w")

for url in urls:

	print("Processing: " + url)
	driver.get(url)
	file.write(url + ",Unpaid")
	time.sleep(1)
	phones = driver.find_elements_by_class_name("phone-swap")
	for phone in phones:
		print("Unpaid: " + phone.text)
		file.write(phone.text + ",")



	driver.get(url + "?provider=google")
	file.write("Paid,")
	time.sleep(1)
	phones = driver.find_elements_by_class_name("phone-swap")
	for phone in phones:
		print("Paid: " + phone.text)
		file.write(phone.text + ",")
	
	file.write("\n")

file.close
driver.quit()
