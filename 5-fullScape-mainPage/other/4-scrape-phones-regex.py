from selenium import webdriver
import tldextract
import re, time

#url = "https://www.affordabledentures.com/office/mesquite/"
#url = "https://budgetblinds.com/manhattan"
url = "https://www.handymanmatters.com/offices/scottsdale/"


driver = webdriver.Chrome()
driver.get(url)

content = driver.find_element_by_tag_name("body")
phones = re.findall(r'(\d\d\d-\d\d\d-\d\d\d\d)', content.text)
for phone in phones:
	print("Unpaid: " + phone)

driver.get(url + "?provider=google")
content = driver.find_element_by_tag_name("body")
phones = re.findall(r"(\d\d\d-\d\d\d-\d\d\d\d)", content.text)
for phone in phones:
	print("Paid: " + phone)

driver.close()

