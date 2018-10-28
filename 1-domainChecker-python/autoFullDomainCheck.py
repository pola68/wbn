import requests, dns.resolver, tldextract, time, psycopg2, sys
sys.path.append('/tools')
import mySetup
from pydrive.drive import GoogleDrive
from pydrive.auth import GoogleAuth
gauth = GoogleAuth(); gauth.LocalWebserverAuth(); drive = GoogleDrive(gauth)

corporateID = "767,203,214,399"
sqlLimit = 10000

#Connecting to Postgres Natpal DB to pull list of domains
try:
	conn=psycopg2.connect( host="coredb2.prod.yodle.com", user=mySetup.natpalDbUsername, password=mySetup.natpalDbPassword, dbname="natpal")
except:
	print("I am unable to connect to the database.")
cur = conn.cursor()
try:
	cur.execute("SELECT cc.id, cc.status, corp.name, cc.name, dom.domainname, cdc.sslinstallstatus, corp.id from control.corporate_relationship corp join control.franchisemasteraccount_client fma on corp.fma_id = fma.franchisemasteraccount_id join control.client cc on fma.franchisechildren_id = cc.id left join control.domainname dom on dom.id = cc.adversitedomainid left join control.domainnameconfiguration cdc on cdc.domainname_id = dom.id WHERE cc.status = 'LIVE' LIMIT {sqlLimit}".format(**vars()))
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
	print("Number of domains to check: " + str(len(rows)))
except:
	print("Cannot run DB query")


def review_domain(url):
	if "http" in url:
		url = url
	else:
		url = 'http://' + url

	try:
		r = requests.get(url)
		#r = requests.get(url)
		print("Processing " + url)


		if len(r.history) > 0:
			chain = ""
			code = r.history[0].status_code
			final_url = r.url
			final_code = r.status_code
			for resp in r.history:
				chain += resp.url + " | "
			
			list = tldextract.extract(final_url)
			final_domain = list.domain + '.' + list.suffix
			for x in dns.resolver.query(final_domain, 'A'):
				url_ip = x.to_text()
			for y in dns.resolver.query(final_domain, 'NS'):
				url_ns = y.to_text()

			return str(code) + ',' + str(len(r.history)) + ',' + chain + ',' + final_url + ',' + str(final_code) + "," + url_ip + ',' + url_ns
		else:
			final_url = r.url
			final_code = r.status_code
			list = tldextract.extract(final_url)
			final_domain = list.domain + '.' + list.suffix
			for x in dns.resolver.query(final_domain, 'A'):
				url_ip = x.to_text()
			try:
				for y in dns.resolver.query(final_domain, 'NS'):
					url_ns = y.to_text()
			except:
				url_ns = "DNS Not Found"
			
			return str(r.status_code) + ',,,' + final_url + ',' + str(final_code) + ',' + url_ip + ',' + url_ns
	except requests.ConnectionError:
		print("Error: failed to connect.")
		return '0,0,0,0,0,0,0'

timestr = time.strftime("%Y-%m-%d___%H-%M-%S")
input_file = 'urls_to_be_checked.txt'
output_file = 'output/domain-checkers-output-' + timestr + '.csv'

g_file = drive.CreateFile({"parents": [{"kind": "drive#fileLink", "id": '19kzjQTNCnfJGwIGitpD2Z4tE91rLL_29'}], 'title': 'fullDomainDNScheck-'+timestr+'.xls', 'mimeType': 'application/vnd.openxmlformats-officedocument.wordprocessingml.document'}) 
g_content = ""

with open(output_file, 'w') as o_file:
	file_header = 'Corp ID,Corp Name,Client ID,Client Name,URL,Status,Number of redirects,Redirect Chain,Final URL,Final URL Status,Final URL IP,Final URL NS,\n'
	o_file.write(file_header)
	g_content += (file_header)
	f = open(input_file, "r")
	lines = f.read().splitlines()
	for url, corpId, corpName, clientid, clientName in zip(urls, corpIds, corpNames, clientids, clientNames):
		if url is None:
			url = "no-domain.com"
		else:
			url = url
		clientName = clientName.replace(",", "")
		code = review_domain(url)
		final_results = str(corpId) + "," + corpName + "," + str(clientid) + "," + clientName + "," + url + "," + str(code) + ",\n"
		o_file.write(final_results)
		g_content += (final_results)
	f.close()
	g_file.SetContentString(g_content)
	g_file.Upload({'convert' : True})




