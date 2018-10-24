from selenium import webdriver
#import tldextract
from urllib.parse import urlparse
import time

#depot = DepotManager.get()
driver = webdriver.Chrome()
#driver.set_window_size(400, 800) # set the window size that you need 

inputfile = open("input_yl_urls.txt")
urls = [url.strip() for url in inputfile.readlines()]

url = urls[0]

if "http" in url:
	url = url
else:
	url = 'http://' + url

driver.get(url)
driver.find_element_by_id("usernameForm").click()
driver.find_element_by_id("usernameForm").clear()
driver.find_element_by_id("usernameForm").send_keys("mswiader@yodle.com")
driver.find_element_by_id("password").click()
driver.find_element_by_id("password").clear()
driver.find_element_by_id("password").send_keys("password")
driver.find_element_by_xpath("(.//*[normalize-space(text()) and normalize-space(.)='Stay Logged In'])[1]/following::input[1]").click()
time.sleep(2)



for url in urls:
	
	if "http" in url:
		url = url
	else:
		url = 'http://' + url
	
	driver.get(url)
	test = driver.find_element_by_xpath("(.//*[normalize-space(text()) and normalize-space(.)='Segment:'])[1]/following::span[1]").text
	clientiddd = driver.find_element_by_id("filterText").get_attribute("value")
	print(test + " " + clientiddd)

driver.quit()