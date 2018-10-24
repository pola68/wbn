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

inputfile = open("input_general_source.txt")
urls = [url.strip() for url in inputfile.readlines()]

driver = webdriver.Chrome()
#driver.set_window_size(1024, 768) # set the window size that you need 
counter = 0
for url in urls:
	counter = counter + 1
	print("Processing: " + url)
	driver.get(url)
	driver.find_element_by_xpath("(.//*[normalize-space(text()) and normalize-space(.)='Fees'])[2]/following::a[1]").click()
	driver.find_element_by_id("FullName").click()
	driver.find_element_by_id("FullName").clear()
	driver.find_element_by_id("FullName").send_keys("Testing")
	driver.find_element_by_id("PhoneNumber").clear()
	driver.find_element_by_id("PhoneNumber").send_keys("555-555-5555")
	driver.find_element_by_id("Email Address").clear()
	driver.find_element_by_id("Email Address").send_keys("test@yodle.com")
	driver.find_element_by_xpath('//*[@id="HowCanHelp"]/option[3]')
	driver.find_element_by_link_text("28").click()
	driver.find_element_by_id("Comments").click()
	driver.find_element_by_id("Comments").clear()
	driver.find_element_by_id("Comments").send_keys("Please disregard.")
	driver.find_element_by_id("submit").click()


driver.quit()
