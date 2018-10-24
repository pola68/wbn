from selenium import webdriver
import time, re

#depot = DepotManager.get()

inputfile = open("input_urls.txt")
urls = [url.strip() for url in inputfile.readlines()]

driver = webdriver.Chrome()
#driver.set_window_size(400, 800) # set the window size that you need 

for url in urls:
	print("Processing: " + url)
	driver.get(url)
	driver.find_element_by_id("usernameForm").click()
	driver.find_element_by_id("usernameForm").clear()
	driver.find_element_by_id("usernameForm").send_keys("")
	driver.find_element_by_id("password").clear()
	driver.find_element_by_id("password").send_keys("")
	driver.find_element_by_xpath("(.//*[normalize-space(text()) and normalize-space(.)='Stay Logged In'])[1]/following::input[1]").click()
	driver.find_element_by_link_text("Call Tracking").click()
	driver.find_element_by_link_text("6613909458").click()
	driver.find_element_by_id("whisperOn1").click()
	time.sleep(3)
	#driver.find_element_by_xpath('//*[@id="saveChanges"]').click()
	driver.find_element_by_css_selector(".positive").click()
	#driver.find_element_by_id("saveChanges").click()
	driver.find_element_by_link_text("Domain & Sites").click()
	time.sleep(3)


driver.quit()