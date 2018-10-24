from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoAlertPresentException
import unittest, time, re

#depot = DepotManager.get()

inputfile = open("input_urls.txt")
urls = [url.strip() for url in inputfile.readlines()]

driver = webdriver.Chrome()
#driver.set_window_size(400, 800) # set the window size that you need 

for url in urls:
	print("Processing: " + url)
	driver.get(url)
	time.sleep(1)
	driver.find_element_by_xpath('//*[@id="local-nav-wrap"]/div[2]/nav/ul/li[6]/a').click()
	driver.find_element_by_xpath("(.//*[normalize-space(text()) and normalize-space(.)='Name'])[2]/following::input[1]").click()
	driver.find_element_by_xpath("(.//*[normalize-space(text()) and normalize-space(.)='Name'])[2]/following::input[1]").clear()
	driver.find_element_by_xpath("(.//*[normalize-space(text()) and normalize-space(.)='Name'])[2]/following::input[1]").send_keys("Test")
	driver.find_element_by_xpath("(.//*[normalize-space(text()) and normalize-space(.)='Phone Number'])[2]/following::input[1]").clear()
	driver.find_element_by_xpath("(.//*[normalize-space(text()) and normalize-space(.)='Phone Number'])[2]/following::input[1]").send_keys("555-444-3333")
	driver.find_element_by_xpath("(.//*[normalize-space(text()) and normalize-space(.)='Zip Code'])[2]/following::input[1]").clear()
	driver.find_element_by_xpath("(.//*[normalize-space(text()) and normalize-space(.)='Zip Code'])[2]/following::input[1]").send_keys("11101")
	driver.find_element_by_xpath("(.//*[normalize-space(text()) and normalize-space(.)='Email Address'])[2]/following::input[1]").clear()
	driver.find_element_by_xpath("(.//*[normalize-space(text()) and normalize-space(.)='Email Address'])[2]/following::input[1]").send_keys("test@yodle.com")
	driver.find_element_by_xpath("(.//*[normalize-space(text()) and normalize-space(.)='Company Name'])[2]/following::input[1]").clear()
	driver.find_element_by_xpath("(.//*[normalize-space(text()) and normalize-space(.)='Company Name'])[2]/following::input[1]").send_keys("Test")
	driver.find_element_by_xpath("(.//*[normalize-space(text()) and normalize-space(.)='Help'])[2]/following::select[1]").click()
	Select(driver.find_element_by_xpath("(.//*[normalize-space(text()) and normalize-space(.)='Help'])[2]/following::select[1]")).select_by_visible_text("Brand Awareness")
	driver.find_element_by_xpath("(.//*[normalize-space(text()) and normalize-space(.)='Message'])[2]/following::textarea[1]").click()
	driver.find_element_by_xpath("(.//*[normalize-space(text()) and normalize-space(.)='Message'])[2]/following::textarea[1]").clear()
	driver.find_element_by_xpath("(.//*[normalize-space(text()) and normalize-space(.)='Message'])[2]/following::textarea[1]").send_keys("Test. Please disregard.")
	driver.find_element_by_xpath("(.//*[normalize-space(text()) and normalize-space(.)='Message'])[2]/following::button[1]").click()


driver.quit()