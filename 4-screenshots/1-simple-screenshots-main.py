from selenium import webdriver
#import tldextract
from urllib.parse import urlparse
import time

#depot = DepotManager.get()

inputfile = open("input_screenshots_urls.txt")
urls = [url.strip() for url in inputfile.readlines()]



driver = webdriver.Chrome()
#driver.set_window_size(400, 800) # set the window size that you need 

for url in urls:
	print("Taking screenshot: " + url)
	
	if "http" in url:
		url = url
	else:
		url = 'http://' + url
	
	driver.get(url)
	maindomain = urlparse(url).netloc
	path = urlparse(url).path
	pathelements = path.split("/")
	grupa = ""
	for pathelement in pathelements:
		grupa = grupa + "_" + pathelement

	time.sleep(1)
	driver.save_screenshot("output/" + maindomain + grupa + ".png")

driver.quit()