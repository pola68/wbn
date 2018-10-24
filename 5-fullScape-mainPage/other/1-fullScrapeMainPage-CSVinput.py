# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoAlertPresentException
import unittest, time, re, csv, requests, tldextract, dns.resolver, psycopg2
from urllib.parse import urlparse


#Checking if imported URL has http/https protocol
def url_check(url):
	if "http" in url:
		url = url
	else:
		url = 'http://' + url
	return url

#Finding phones numbers on websites
def find_phones():
	content = driver.find_element_by_tag_name("body")
	phones = re.findall(r'(\d\d\d.\d\d\d.\d\d\d\d)', content.text)
	return phones


#Opening CSV with client information
f = open("input_urls.csv")
csv_f = csv.reader(f)
clientids = []
urls = []
for row in csv_f:
	clientids.append(row[0])
	urls.append(row[1])
f.close()


file = open("output/output_phone_scrape.csv", "w")
driver = webdriver.Chrome()
item_counter = 0
#Set Window Size
#



for clientid, url in zip(clientids, urls):

	item_counter = item_counter + 1
	print("\n" + str(item_counter) + "/" + str(len(clientids)) + " Processing: " + url)
	url = url_check(url)
	driver.get(url)

#Checking Website HTTP Status, A / NS Records
	try:
		r = requests.get(url)
		if len(r.history) > 0:
			initial_status = requests.get(url).history[0].status_code
		else:
			initial_status = r.status_code
		final_status = requests.get(url).status_code
		final_url = driver.current_url
		list = tldextract.extract(final_url)
		domain_to_check = list.domain + '.' + list.suffix
		for x in dns.resolver.query(domain_to_check, 'A'):
			url_ip = x.to_text()
		for y in dns.resolver.query(domain_to_check, 'NS'):
			url_ns = y.to_text()
		print("HTTP Status:" + str(initial_status) + " " + str(final_status) + " A:" + url_ip + " NS:" + url_ns)
	except requests.ConnectionError:
		print("HTTP Status: Connection Error")	
		initial_status = 0; final_status = 0


#Scraping Unpaid Numbers (Desktop)
	driver.set_window_size(1200, 800)
	phones = find_phones()
	if not phones:
		print(clientid + " No Desktop Unpaid Numbers")
		file.write(clientid + "," + url + ",Desktop Unpaid,No Desktop Unpaid Numbers,")
	else:
		file.write(clientid + "," + url + ",Desktop Unpaid," + phones[0] + ",")
		for phone in phones:
			print(clientid + " Desktop Unpaid: " + phone)

#Taking Screenshot
	maindomain = urlparse(url).netloc
	path = urlparse(url).path
	pathelements = path.split("/")
	grupa = ""
	for pathelement in pathelements:
		grupa = grupa + "_" + pathelement

	print("Taking Screenshot Of: " + url)
	time.sleep(1)
	driver.save_screenshot("output/" + clientid + "-" + maindomain + grupa + ".png")


#Scraping Unpaid Numbers (Mobile)
	driver.set_window_size(400, 600)
	phones = find_phones()
	if not phones:
		print(clientid + " No Mobile Unpaid Numbers")
		file.write("Mobile Unpaid,No Mobile Unpaid Numbers,")
	else:
		file.write("Mobile Unpaid," + phones[0] + ",")
		for phone in phones:
			print(clientid + " Mobile Unpaid: " + phone)


#Scraping Paid Numbers (Desktop)
	driver.get(url + "?provider=google")
	driver.set_window_size(1200, 800)
	time.sleep(3)
	phones = find_phones()
	if len(phones) == 0:
		print(clientid + " No Desktop Paid Numbers")
		file.write("Desktop Paid,No Desktop Paid Numbers,")
	else:
		file.write("Desktop Paid," + phones[0] + ",")
		for phone in phones:
			print(clientid + " Desktop Paid: " + phone)


#Scraping Paid Numbers (Mobile)
	driver.set_window_size(400, 600)
	phones = find_phones()
	if len(phones) == 0:
		print(clientid + " No Mobile Paid Numbers")
		file.write("Mobile Paid,No Mobile Paid Numbers,")
	else:
		file.write("Mobile Paid," + phones[0] + ",")
		for phone in phones:
			print(clientid + " Mobile Paid: " + phone)

#Detecting Session Tracking Code
	source_code = driver.page_source
	if "natpal" in source_code:
		print("Tracking Session Code: FOUND")
		file.write("Session Code There,")
	else:
		print("Tracking Session Code: NOT FOUND")
		file.write("No Session Code,")


#Gathering Data from DB 
	try:
		conn=psycopg2.connect( host="coredb2.prod.yodle.com", user="", password="", dbname="natpal")
	except:
		print("I am unable to connect to the database.")

	cur = conn.cursor()

# Retrieving Unpaid Number And "Show Destination" Flag From DB
	try:
		cur.execute("SELECT num.number, ctc.usedestinationnumber FROM control.calltrackingnumber num JOIN control.calltrackingnumberconfiguration conf ON conf.id = num.calltrackingnumberconfiguration_id LEFT JOIN control.ctcattributionconfig ctc on ctc.id = conf.attributionconfig_id WHERE ctc.secondaryattribution is null and ctc.primaryattribution = 'unpaid' and conf.client_id = {clientid}".format(**vars()))
		rows = cur.fetchall()
		db_unpaidNumber = []; db_unpaidNumber = rows[0][0]
		db_unpaidShowDest = []; db_unpaidShowDest = rows[0][1]
		print("DB Unpaid number: " + db_unpaidNumber + " Show Destination: " + str(db_unpaidShowDest))
		file.write("DB Unpaid," + str(db_unpaidNumber) + "," + str(db_unpaidShowDest) + ",")
		#cur.close()
	except:
		print("DB Unpaid number: Not Found")
		file.write("DB Unpaid,No DB Unpaid Number,")

# Retrieving Paid Number From DB
	try:
		cur.execute("SELECT conf.client_id, num.number, ctc.primaryattribution, ctc.secondaryattribution FROM control.calltrackingnumber num JOIN control.calltrackingnumberconfiguration conf ON conf.id = num.calltrackingnumberconfiguration_id LEFT JOIN control.ctcattributionconfig ctc on ctc.id = conf.attributionconfig_id WHERE ctc.secondaryattribution is null and ctc.primaryattribution = 'paid' and conf.client_id = {clientid}".format(**vars()))
		rows = cur.fetchall()
		db_paidNumber = []; db_paidNumber = rows[0][1]
		print("DB Paid number: " + db_paidNumber)
		file.write("DB Paid," + str(db_paidNumber) + ",")
		#cur.close()
	except:
		print("DB Paid number: Not Found")
		file.write("DB Paid,No DB Paid Number,")

# Retrieving Paid Number From DB
	try:
		cur.execute("SELECT displayname from snapshot.client_product_status ps join enum.product_status eps on eps.id = ps.status join control.product cp on cp.id = ps.product_id where displayname = 'Sponsored' and eps.status = 'Live' and date = '2018-09-23' and client_id = {clientid}".format(**vars()))
		rows = cur.fetchall()
		db_ppcProduct = []; db_ppcProduct = rows[0][0]
		print("PPC Product: " + db_ppcProduct)
		file.write(str(db_ppcProduct) + ",")
		#cur.close()
	except:
		print("PPC Product: Not Found")
		file.write("PPC Product Not Found,")

	conn.close()



#Checking Whether Final URL Has HTTPS Or Not
	final_url = driver.current_url
	print("Final url: " + final_url)
	url_protocol = urlparse(final_url).scheme
	file.write(url_protocol + "," + final_url + "," + str(initial_status) + "," + str(final_status) + "," + url_ip + "," + url_ns + "\n")


file.close
driver.quit()
print("All work completed!\n")
