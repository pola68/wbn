#!/usr/bin/env python

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium import webdriver

# Start the WebDriver and load the page
wd = webdriver.Firefox()
wd.get("https://stats.uptimerobot.com/gL1OnswNO")

# Wait for the dynamically loaded elements to show up
WebDriverWait(wd, 10).until(
    EC.visibility_of_element_located((By.XPATH, '//*[@id="overall-uptime"]/ul/li[1]/strong')))

# And grab the page HTML source
html_page = wd.page_source


text1 = html_page.find_element_by_xpath('//*[@id="overall-uptime"]/ul/li[3]/strong')
print(text1.text)
wd.quit()

"""
from selenium import webdriver
from selenium.webdriver.common.by import By
from urllib.parse import urlparse
import time, requests
from lxml import html


pageContent=requests.get('https://stats.uptimerobot.com/gL1OnswNO')
tree = html.fromstring(pageContent.content)

sevenDays = tree.xpath('//*[@id="overall-uptime"]/ul/li[1]/strong')

print(sevenDays)



driver = webdriver.Firefox()
driver.get("https://stats.uptimerobot.com/gL1OnswNO")


source_code = driver.page_source
print(source_code)




text1 = driver.find_element_by_xpath('//*[@id="overall-uptime"]/ul/li[3]/strong')
text2 = driver.find_element_by_xpath('//*[@id="overall-uptime"]/h2')

print(text1.text)
print(text2.text)

driver.quit()
"""

