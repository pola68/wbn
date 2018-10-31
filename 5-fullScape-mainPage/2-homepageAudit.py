# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoAlertPresentException
import unittest, time, datetime, re, csv, requests, tldextract, dns.resolver, psycopg2, sys, sqlite3, datetime, smtplib
from urllib.parse import urlparse
sys.path.append('/tools')
import mySetup
from pydrive.drive import GoogleDrive
from pydrive.auth import GoogleAuth
gauth = GoogleAuth(); gauth.LocalWebserverAuth(); drive = GoogleDrive(gauth)

corporateID = sys.argv[1]
sqlLimit = sys.argv[2]

#Opening SQLite Connection
sqlite_connection = sqlite3.connect('database.db', timeout=10); c = sqlite_connection.cursor()

#Create QA session ID
czas = time.time()
qa_session_id = datetime.datetime.fromtimestamp(czas).strftime('%Y%m%d%H%M%S')
print(qa_session_id)


#Checking if imported URL has http/https protocol
def url_check(url):
	if "http" in url:
		url = url
	else:
		url = 'http://' + url
	return url

#Finding phones numbers on websites
def find_phones():
	try:
		content = driver.find_element_by_tag_name("body")
		phones = re.findall(r'(\d\d\d.\d\d\d.\d\d\d\d)', content.text)
	except:
		phones = []
	return phones


#Connecting to Postgres Natpal DB to pull list of accounts
try:
	conn=psycopg2.connect(host=mySetup.natpalHost, user=mySetup.natpalDbUsername, password=mySetup.natpalDbPassword, dbname=mySetup.natpalDBname)
except:
	print("I am unable to connect to the database.")
cur = conn.cursor()
try:
	cur.execute("SELECT cc.id, cc.status, corp.name, cc.name, dom.domainname, cdc.sslinstallstatus, corp.id from control.corporate_relationship corp join control.franchisemasteraccount_client fma on corp.fma_id = fma.franchisemasteraccount_id join control.client cc on fma.franchisechildren_id = cc.id left join control.domainname dom on dom.id = cc.adversitedomainid left join control.domainnameconfiguration cdc on cdc.domainname_id = dom.id WHERE cc.status = 'LIVE' and corp.id in ({corporateID}) LIMIT {sqlLimit}".format(**vars()))
	rows = list(cur.fetchall())
	clientids = []; clientStatuses = []; corpNames = []; clientNames = []; urls = []; sslStatuses = []; corpIds = []
	for row in rows:
		clientids.append(row[0])
		clientStatuses.append(row[1])
		corpNames.append(row[2])
		clientNames.append(row[3])
		urls.append(row[4])
		sslStatuses.append(row[5])
		corpIds.append(row[6])

	cur.close()
except:
	print("Cannot run DB query")


"""
#Opening CSV with client information
f = open("input_urls.csv")
csv_f = csv.reader(f)
clientids = []
urls = []
for row in csv_f:
	clientids.append(row[0])
	urls.append(row[1])
f.close()
"""

#Opening Output File
file = open("output/" + corporateID + "-output_phone_scrape.csv", "w")
file.write("Audit Timestamp,Corp Name,Client ID,Client Name,YL Status,Input URL,Desktop Unpaid CTN,Mobile Unpaid CTN,Desktop Paid CTN,Mobile Paid CTN,DB Unpaid CTN,Show Destination,DB Paid CTN,PPC,YL SSL Status,Final URL,Initial Status, Final Status,Final URL IP,Final URL NS,Analysis - Desktop Unpaid CTN,Analysis - Mobile Unpaid CTN,Analysis - Desktop Paid CTN,Analysis - Mobile Paid CTN,PPC Product,Session Tracking Code,Web Using SSL, Can SSL Be installed\n")


driver = webdriver.Chrome()
item_counter = 0

#---------------Loop Starts Here------------------------
for clientid, clientStatus, corpName, clientName, url, sslStatus, corpId in zip(clientids, clientStatuses, corpNames, clientNames, urls, sslStatuses, corpIds):

	clientid = str(clientid) #converting into string

	
#Protection For Accounts With No Domain
	if url == None:
		url = "None"
		db_is_domain_in = "no"
	else:
		db_is_domain_in = "yes"
		url = str(url)

#Removing commas from Client Name
	clientName = clientName.replace(",", "") 

#Creating timestamp
	czas = time.time()
	timestamp = datetime.datetime.fromtimestamp(czas).strftime('%Y-%m-%d %H:%M:%S')

#Initial Account Printout
	item_counter = item_counter + 1
	print("\n" + str(item_counter) + "/" + str(len(clientids)) + "\n" + timestamp + "\nClient ID: " + clientid + "\nClient Name: " + clientName + "\nURL: " + url)
	file.write(timestamp + ",")

#Adding http if it doesn't exist 
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
		try:
			for y in dns.resolver.query(domain_to_check, 'NS'):
				url_ns = y.to_text()
		except:
			url_ns = "NS Not Found"	
		print("HTTP Status:" + str(initial_status) + " " + str(final_status) + " A:" + url_ip + " NS:" + url_ns)
	except requests.ConnectionError:
		print("HTTP Status: Connection Error")	
		initial_status = "0"; final_status = "0"; url_ip = "0"; url_ns = "0"; final_url = driver.current_url


#Scraping Unpaid Numbers (Desktop)
	driver.set_window_size(1200, 800)
	time.sleep(3)
	phones = find_phones()
	if not phones:
		web_desk_unpaid_num = "0"
		print(clientid + " No Desktop Unpaid Numbers")
		file.write(corpName + "," + clientid + "," + clientName + "," + clientStatus + "," + url + ",No Desktop Unpaid Numbers,")
	else:
		web_desk_unpaid_num = phones[0]
		file.write(corpName + "," + clientid + "," + clientName + "," + clientStatus + "," + url + "," + web_desk_unpaid_num + ",")
		for phone in phones:
			print(clientid + " Desktop Unpaid: " + phone)


#Taking Screenshot
#	maindomain = urlparse(url).netloc
#	path = urlparse(url).path
#	pathelements = path.split("/")
#	grupa = ""
#	for pathelement in pathelements:
#		grupa = grupa + "_" + pathelement
#
#	print("Taking Screenshot Of: " + url)
#	time.sleep(1)
#	driver.save_screenshot("output/" + clientid + "-" + maindomain + grupa + ".png")



#Scraping Unpaid Numbers (Mobile)
	driver.set_window_size(400, 600)
	time.sleep(3)
	phones = find_phones()
	if not phones:
		web_mobile_unpaid_num = "0"
		print(clientid + " No Mobile Unpaid Numbers")
		file.write("No Mobile Unpaid Numbers,")
	else:
		web_mobile_unpaid_num = phones[0]
		file.write(web_mobile_unpaid_num + ",")
		for phone in phones:
			print(clientid + " Mobile Unpaid: " + phone)


#Scraping Paid Numbers (Desktop)
	driver.quit()
	driver = webdriver.Chrome()
	driver.set_window_size(1200, 800)
	driver.get(url + "?provider=google")
	time.sleep(5)
	phones = find_phones()
	if len(phones) == 0:
		web_desk_paid_num = "0"
		print(clientid + " No Desktop Paid Numbers")
		file.write("No Desktop Paid Numbers,")
	else:
		web_desk_paid_num = phones[0]
		file.write(web_desk_paid_num + ",")
		for phone in phones:
			print(clientid + " Desktop Paid: " + phone)


#Scraping Paid Numbers (Mobile)
	driver.set_window_size(400, 600)
	time.sleep(3)
	phones = find_phones()
	if len(phones) == 0:
		web_mobile_paid_num = "0"
		print(clientid + " No Mobile Paid Numbers")
		file.write("No Mobile Paid Numbers,")
	else:
		web_mobile_paid_num = phones[0]
		file.write(web_mobile_paid_num + ",")
		for phone in phones:
			print(clientid + " Mobile Paid: " + phone)


#Connecting To Natpal DB
	try:
		conn=psycopg2.connect( host="coredb2.prod.yodle.com", user="mswiader", password="Korana17", dbname="natpal")
	except:
		print("I am unable to connect to the database.")
	cur = conn.cursor()

# Retrieving Unpaid Number And "Show Destination" Flag From DB
	try:
		cur.execute("SELECT num.number, ctc.usedestinationnumber FROM control.calltrackingnumber num JOIN control.calltrackingnumberconfiguration conf ON conf.id = num.calltrackingnumberconfiguration_id LEFT JOIN control.ctcattributionconfig ctc on ctc.id = conf.attributionconfig_id WHERE conf.deleted = 'false' and ctc.secondaryattribution is null and ctc.primaryattribution = 'unpaid' and conf.client_id = {clientid}".format(**vars()))
		rows = cur.fetchall()
		db_unpaidNumber = []; db_unpaidNumber = rows[0][0]
		db_unpaidShowDest = []; db_unpaidShowDest = rows[0][1]
		print("DB Unpaid number: " + db_unpaidNumber + " Show Destination: " + str(db_unpaidShowDest))
		file.write(str(db_unpaidNumber) + "," + str(db_unpaidShowDest) + ",")
	except:
		db_unpaidNumber = "No DB Unpaid Number"
		db_unpaidShowDest = "false"
		print("DB Unpaid number: Not Found")
		file.write("No DB Unpaid Number,")

# Retrieving Paid Number From DB
	try:
		cur.execute("SELECT conf.client_id, num.number, ctc.primaryattribution, ctc.secondaryattribution FROM control.calltrackingnumber num JOIN control.calltrackingnumberconfiguration conf ON conf.id = num.calltrackingnumberconfiguration_id LEFT JOIN control.ctcattributionconfig ctc on ctc.id = conf.attributionconfig_id WHERE conf.deleted = 'false' and ctc.secondaryattribution is null and ctc.primaryattribution = 'paid' and conf.client_id = {clientid}".format(**vars()))
		rows = cur.fetchall()
		db_paidNumber = []; db_paidNumber = rows[0][1]
		print("DB Paid number: " + db_paidNumber)
		file.write(str(db_paidNumber) + ",")
	except:
		db_paidNumber = "No DB Paid Number"
		print("DB Paid number: Not Found")
		file.write("No DB Paid Number,")

# Retrieving PPC Paid Product From DB
	prev_date = datetime.datetime.today() - datetime.timedelta(days=1)
	prev_date_format = prev_date.strftime ('%Y-%m-%d') 

	try:
		cur.execute("SELECT displayname from snapshot.client_product_status ps join enum.product_status eps on eps.id = ps.status join control.product cp on cp.id = ps.product_id where displayname = 'Sponsored' and eps.status = 'Live' and date = {prev_date_format} and client_id = {clientid}".format(**vars()))
		rows = cur.fetchall()
		db_ppcProduct = []; db_ppcProduct = rows[0][0]
		print("PPC Product: " + db_ppcProduct)
		file.write(str(db_ppcProduct) + ",")
	except:
		print("PPC Product: Not Found")
		file.write("PPC Not Found,")
		db_ppcProduct = "PPC Not Found"

	conn.close()


#Adding couple of URL metrics
	file.write(str(sslStatus) + "," + final_url + "," + str(initial_status) + "," + str(final_status) + "," + url_ip + "," + url_ns + ",")


#-----------Analysis---------------------------------------------

#Analysis - Does Unpaid Desktop Number Matches Yodle Live
	web_desk_unpaid_num = web_desk_unpaid_num.replace("-", "")
	web_desk_unpaid_num = web_desk_unpaid_num.replace(".", "")
	if db_unpaidNumber == web_desk_unpaid_num:
		analys_unpaid_desk_match = "yes"
		file.write("yes,")
	else:
		analys_unpaid_desk_match = "no"
		file.write("no,")

#Analysis - Does Unpaid Mobile Number Matches Yodle Live
	web_mobile_unpaid_num = web_mobile_unpaid_num.replace("-", "")
	web_mobile_unpaid_num = web_mobile_unpaid_num.replace(".", "")
	if db_unpaidNumber == web_mobile_unpaid_num:
		analys_unpaid_mobile_match = "yes"
		file.write("yes,")
	else:
		analys_unpaid_mobile_match = "no"
		file.write("no,")

#Analysis - Does Paid Desktop Number Matches Yodle Live
	web_desk_paid_num = web_desk_paid_num.replace("-", "")
	web_desk_paid_num = web_desk_paid_num.replace(".", "")
	if db_paidNumber == web_desk_paid_num:
		analys_paid_desk_match = "yes"
		file.write("yes,")
	else:
		analys_paid_desk_match = "no"
		file.write("no,")

#Analysis - Does Paid Mobile Number Matches Yodle Live
	web_mobile_paid_num = web_mobile_paid_num.replace("-", "")
	web_mobile_paid_num = web_mobile_paid_num.replace(".", "")
	if db_paidNumber == web_mobile_paid_num:
		analys_paid_mobile_match = "yes"
		file.write("yes,")
	else:
		analys_paid_mobile_match = "no"
		file.write("no,")

#Analysis - Does Paid Product Exist
	try:
		file.write(str(db_ppcProduct) + ",")
	except:
		file.write("No PPC Product,")

#Analysis - Is Paid CTN config proper
	if (db_ppcProduct == "Sponsored" and web_desk_paid_num == "0"):
		is_paid_ctn_config_proper = "no"
	else:
		is_paid_ctn_config_proper = "yes"


#Analysis - Is website working properly
	if final_status == 200:
		is_website_up = "yes"
		print("Is website up: " + is_website_up + " - " + str(final_status))
	else:
		is_website_up = "no"
		print("Is website up: " + is_website_up + " - " + str(final_status))

#Analysis - Is website redirected to another domain
	initial_root_domain = (urlparse(url).netloc + urlparse(url).path)
	final_root_domain = (urlparse(final_url).netloc + urlparse(final_url).path)
	final_root_domain = final_root_domain.replace("www.", "")
	print("Initial root url: %s\nFinal root url: %s" % (initial_root_domain, final_root_domain))
	if initial_root_domain == final_root_domain:
		is_redirecting = "no"
	else:
		is_redirecting = "yes"

#Analysis - Does Session Tracking Code Exist
	source_code = driver.page_source
	if "labs.natpal.com/trk/" in source_code:
		session_tr_code_stat = "yes"
		print("Tracking Session Code: %s" % session_tr_code_stat)
		file.write(session_tr_code_stat + ",")
	else:
		session_tr_code_stat = "no"
		print("Tracking Session Code: %s" % session_tr_code_stat)
		file.write(session_tr_code_stat + ",")

#Checking Whether Final URL Has HTTPS Or Not
	final_url = driver.current_url
	print("Final url: " + final_url)
	url_protocol = urlparse(final_url).scheme
	if url_protocol == "https":
		web_using_ssl = "yes"
		file.write(web_using_ssl + ",")		
	else:
		web_using_ssl = "no"
		file.write(web_using_ssl + ",")

#Checking If SSL can be installed (domain pointing to our NS)
	our_dns = ['ns3a.dns-host.com.','ns3b.dns-host.com.','ns4a.dns-host.com.','ns4b.dns-host.com.']
	if url_ns in our_dns:
		can_ssl_be_installed = "yes"
		file.write(can_ssl_be_installed + "\n")
	else:
		can_ssl_be_installed = "no"
		file.write(can_ssl_be_installed + "\n")


#Is acctount error free
	if (db_is_domain_in == "yes" and is_website_up == "yes" and analys_unpaid_desk_match == "yes" and analys_unpaid_mobile_match == "yes" and is_paid_ctn_config_proper == "yes" and session_tr_code_stat == "yes" and web_using_ssl == "yes"):
		is_error_free = "yes"
	else:
		is_error_free = "no"


#Adding record to SQLite DB
	c.execute("INSERT INTO main_audit VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", (qa_session_id, timestamp, corpId, corpName, clientid, clientName, clientStatus, url, web_desk_unpaid_num, web_mobile_unpaid_num, web_desk_paid_num, web_mobile_paid_num, db_unpaidNumber, db_paidNumber, db_unpaidShowDest, db_ppcProduct, sslStatus, final_url, initial_status, final_status, url_ip, url_ns, db_is_domain_in, is_website_up, is_redirecting, analys_unpaid_desk_match, analys_unpaid_mobile_match, analys_paid_desk_match, analys_paid_mobile_match, is_paid_ctn_config_proper, session_tr_code_stat, web_using_ssl, can_ssl_be_installed, is_error_free))


#Closing CSV Output File
	file.close




#Closing All Outstanding Resources
# Closing SQLite DB Entries and Connection
sqlite_connection.commit(); #sqlite_connection.close()
driver.quit()
print("All work completed!\n")


#Defining variables before pulling results from SQLite DB
results_summary = "Error type,qa_session_id,audit_timestamp,corp_id,corp_name,client_id,client_name,client_status,client_url,web_unpaid_desk_num,web_unpaid_mobile_num,web_paid_desk_num,web_paid_mobile_num,db_unpaid_num,db_paid_num,db_show_dest_num,db_paid_product,db_ssl_status,final_url,initial_http_status,final_http_status,final_url_ip,final_url_ns,is_domain_in_yl,is_website_live,is_website_redirected,is_unpaid_desk_match,is_unpaid_mob_match,is_paid_desk_match,is_paid_mob_match,is_paid_ctn_config_proper,is_session_tracking_on,is_https_on,is_https_doable,is_error_free\n"

main_query = "SELECT qa_session_id, audit_timestamp, corp_id, corp_name, client_id, client_name, client_status, client_url, web_unpaid_desk_num, web_unpaid_mobile_num, web_paid_desk_num, web_paid_mobile_num, db_unpaid_num, db_paid_num, db_show_dest_num, db_paid_product, db_ssl_status, final_url, initial_http_status, final_http_status, final_url_ip, final_url_ns, is_domain_in_yl, is_website_live, is_website_redirected, is_unpaid_desk_match, is_unpaid_mob_match, is_paid_desk_match, is_paid_mob_match, is_paid_ctn_config_proper, is_session_tracking_on, is_https_on, is_https_doable, is_error_free from main_audit where qa_session_id = (select max(qa_session_id) from main_audit)"

#Pulling all accounts with errors
sqlite_connection = sqlite3.connect('database.db', timeout=10); c = sqlite_connection.cursor()
c.execute("{main_query} and is_error_free = 'no'".format(**vars()))
total_all_with_errors = c.fetchall()
#results_summary += "\nAll Accounts With Errors (%s)\n" % len(total_all_with_errors)
for row in total_all_with_errors:
	print("%s - %s" % (row[4],row[5]))
	results_summary += "All Errors,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,\n" % (row[0],row[1],row[2],row[3],row[4],row[5],row[6],row[7],row[8],row[9],row[10],row[11],row[12],row[13],row[14],row[15],row[16],row[17],row[18],row[19],row[20],row[21],row[22],row[23],row[24],row[25],row[26],row[27],row[28],row[29],row[30],row[31],row[32],row[33])

#Pulling accounts with "Is domain in YL" error
c.execute("{main_query} and is_domain_in_yl = 'no'".format(**vars()))
all_with_errors = c.fetchall()
#results_summary += "\n\nCheck if domain is in YL for these accounts: (%s)\n" % len(all_with_errors)
for row in all_with_errors:
	results_summary += "Check if domain is in YL,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,\n" % (row[0],row[1],row[2],row[3],row[4],row[5],row[6],row[7],row[8],row[9],row[10],row[11],row[12],row[13],row[14],row[15],row[16],row[17],row[18],row[19],row[20],row[21],row[22],row[23],row[24],row[25],row[26],row[27],row[28],row[29],row[30],row[31],row[32],row[33])

#Pulling accounts with "Is website live" errors
c.execute("{main_query} and is_website_live = 'no'".format(**vars()))
all_with_errors = c.fetchall()
#results_summary += "\n\nCheck if main advertising website is working for these accounts: (%s)\n" % len(all_with_errors)
for row in all_with_errors:
	results_summary += "Check if website is live,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,\n" % (row[0],row[1],row[2],row[3],row[4],row[5],row[6],row[7],row[8],row[9],row[10],row[11],row[12],row[13],row[14],row[15],row[16],row[17],row[18],row[19],row[20],row[21],row[22],row[23],row[24],row[25],row[26],row[27],row[28],row[29],row[30],row[31],row[32],row[33])

#Pulling accounts with "Is upaid desktop matching" errors

c.execute("{main_query} and is_unpaid_desk_match = 'no'".format(**vars()))
all_with_errors = c.fetchall()
#results_summary += "\n\nCheck if UNPAID DESKTOP number is working for these accounts: (%s)\n" % len(all_with_errors)
for row in all_with_errors:
	results_summary += "Check unpaid desktop CTN,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,\n" % (row[0],row[1],row[2],row[3],row[4],row[5],row[6],row[7],row[8],row[9],row[10],row[11],row[12],row[13],row[14],row[15],row[16],row[17],row[18],row[19],row[20],row[21],row[22],row[23],row[24],row[25],row[26],row[27],row[28],row[29],row[30],row[31],row[32],row[33])

#Pulling accounts with "Is upaid mobile matching" errors
c.execute("{main_query} and is_unpaid_mob_match = 'no'".format(**vars()))
all_with_errors = c.fetchall()
#results_summary += "\n\nCheck if UNPAID MOBILE number is working for these accounts: (%s)\n" % len(all_with_errors)
for row in all_with_errors:
	results_summary += "Check unpaid mobile CTN,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,\n" % (row[0],row[1],row[2],row[3],row[4],row[5],row[6],row[7],row[8],row[9],row[10],row[11],row[12],row[13],row[14],row[15],row[16],row[17],row[18],row[19],row[20],row[21],row[22],row[23],row[24],row[25],row[26],row[27],row[28],row[29],row[30],row[31],row[32],row[33])

#Pulling accounts with "Is paid configured properly" errors
c.execute("{main_query} and is_paid_ctn_config_proper = 'no'".format(**vars()))
all_with_errors = c.fetchall()
#results_summary += "\n\nCheck if PAID number is working for these accounts: (%s)\n" % len(all_with_errors)
for row in all_with_errors:
	results_summary += "Check paid CTN,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,\n" % (row[0],row[1],row[2],row[3],row[4],row[5],row[6],row[7],row[8],row[9],row[10],row[11],row[12],row[13],row[14],row[15],row[16],row[17],row[18],row[19],row[20],row[21],row[22],row[23],row[24],row[25],row[26],row[27],row[28],row[29],row[30],row[31],row[32],row[33])

#Pulling accounts with "Is session tracking code configured properly" errors
c.execute("{main_query} and is_session_tracking_on = 'no'".format(**vars()))
all_with_errors = c.fetchall()
#results_summary += "\n\nCheck if SESSION TRACKING CODE present for these accounts: (%s)\n" % len(all_with_errors)
for row in all_with_errors:
	results_summary += "Check session tracking code,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,\n" % (row[0],row[1],row[2],row[3],row[4],row[5],row[6],row[7],row[8],row[9],row[10],row[11],row[12],row[13],row[14],row[15],row[16],row[17],row[18],row[19],row[20],row[21],row[22],row[23],row[24],row[25],row[26],row[27],row[28],row[29],row[30],row[31],row[32],row[33])

#Pulling accounts with "Is website running on SSL" errors
c.execute("{main_query} and is_https_on = 'no'".format(**vars()))
all_with_errors = c.fetchall()
#results_summary += "\n\nCheck if SSL is enabled for these accounts: (%s)\n" % len(all_with_errors)
for row in all_with_errors:
	results_summary += "Check if SSL is enabled,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,\n" % (row[0],row[1],row[2],row[3],row[4],row[5],row[6],row[7],row[8],row[9],row[10],row[11],row[12],row[13],row[14],row[15],row[16],row[17],row[18],row[19],row[20],row[21],row[22],row[23],row[24],row[25],row[26],row[27],row[28],row[29],row[30],row[31],row[32],row[33])

#Pulling accounts where SSL can be fixed
c.execute("{main_query} and is_https_on = 'no' and is_https_doable = 'yes'".format(**vars()))
all_with_errors = c.fetchall()
#results_summary += "\n\nAccount where SSL can be provisioned: (%s)\n" % len(all_with_errors)
for row in all_with_errors:
	results_summary += "Provision SSL,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,\n" % (row[0],row[1],row[2],row[3],row[4],row[5],row[6],row[7],row[8],row[9],row[10],row[11],row[12],row[13],row[14],row[15],row[16],row[17],row[18],row[19],row[20],row[21],row[22],row[23],row[24],row[25],row[26],row[27],row[28],row[29],row[30],row[31],row[32],row[33])




sqlite_connection.close()



#Sending Email
subject = '%s - Audit Results - %s errors' % (corpName, len(total_all_with_errors)) 
body = 'Here are results of the latest audit Enterprise Audit.\n\n' + results_summary
recipients = 'pola68@gmail.com, mswiader@yodle.com'
gmail_user = mySetup.gmailUsername
gmail_pwd = mySetup.gmailPassword
smtpserver = smtplib.SMTP("smtp.gmail.com",587)
smtpserver.ehlo(); smtpserver.starttls(); smtpserver.login(gmail_user, gmail_pwd)
header = 'To:' + recipients + '\n' + 'From: ' + gmail_user + '\n' + 'Subject:' + subject + ' \n'
msg = header + '\n' + body + '\n\n'
smtpserver.sendmail(gmail_user, recipients.split(', '), msg)

#Creating results summary output file
file_summary = open("output/qa_summary - " + corpName + ".csv", "w")
file_summary.write(results_summary)
file_summary.close

#Saving to Google Drive
g_file = drive.CreateFile({"parents": [{"kind": "drive#fileLink", "id": '19kzjQTNCnfJGwIGitpD2Z4tE91rLL_29'}], 'title': 'mainPageQA-'+corpName+' - Accounts With Errors-'+str(len(total_all_with_errors))+'.xls', 'mimeType': 'application/vnd.openxmlformats-officedocument.wordprocessingml.document'}) 
g_file.SetContentString(results_summary)
g_file.Upload({'convert' : True})



