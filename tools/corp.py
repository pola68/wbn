#!/usr/bin/env python
import psycopg2, sys, requests, dns.resolver, tldextract, time
from sty import fg, bg, ef, rs, Rule, Render
sys.path.append('/tools')
import mySetup

#Colors
col1 = fg.white
col2 = ef.bold + fg.li_red

#List microsites under certain corp website
def microSites(corp_input):
	try:
		conn2=psycopg2.connect( host="coredb2.prod.yodle.com", user=mySetup.natpalDbUsername, password=mySetup.natpalDbPassword, dbname="natpal")
	except:
		print("I am unable to connect to the database.")
	cur = conn2.cursor()
	try:
		cur.execute("SELECT corp.id, cc.id, cc.name, cd.domainname, corp.name from control.corporate_relationship corp join control.franchisemasteraccount_client fma on corp.fma_id = fma.franchisemasteraccount_id join control.client cc on fma.franchisechildren_id = cc.id left join control.domainname cd on cd.id = cc.adversitedomainid left join control.domainnameconfiguration cdc on cdc.domainname_id = cd.id {corp_input}".format(**vars()))
		rows = list(cur.fetchall())
		corpIds = []; clientIds = []; clientNames = []; clientDomains = []; corpNames = []
		for row in rows:
			corpIds.append(row[0])
			clientIds.append(row[1])
			clientNames.append(row[2])
			clientDomains.append(row[3])
			corpNames.append(row[4])

		cur.close()
	except:
		print("Cannot run DB query")

	print("-----------------------------------------------------\nCorpID\tCorp Name\tLocID\tLocation Name\tURL")
	
	for corpId, clientId, clientName, clientDomain, corpName in zip(corpIds, clientIds, clientNames, clientDomains, corpNames):
		print(str(corpId) + col2 + " | " + rs.all + str(corpName) + col2 + " | " + rs.all + str(clientId) + col2 + " | " + rs.all + str(clientName) + col2 + " | " + rs.all + str(clientDomain))

	print("\n# of locations in this relationship: " + col1 + str(len(rows)) + rs.all)
	print("-----------------------------------------------------")
	conn2.close

# Local Account Lookup
def localAccountLookup(loc_account_input):
	try:
		conn=psycopg2.connect( host="coredb2.prod.yodle.com", user=mySetup.natpalDbUsername, password=mySetup.natpalDbPassword, dbname="natpal")
	except:
		print("I am unable to connect to the database.")
	cur = conn.cursor()

	#Main Account Info
	try:
		cur.execute("SELECT corp.id, corp.name, cc.id, cc.status, cc.name, cd.domainname, cc.street1, cc.street2, cc.city, cc.state, cc.zipcode, corp.short_name, seg.name, cc.nationalaccount, cc.salesforceid, cc.client_uuid, cc.themekey from control.client cc left join control.franchisemasteraccount_client fma on fma.franchisechildren_id = cc.id left join control.corporate_relationship corp on corp.fma_id = fma.franchisemasteraccount_id left join control.segment seg on seg.id = cc.segment_id left join control.domainname cd on cd.client_id = cc.id where {loc_account_input} order by corp.id".format(**vars()))
		rows = list(cur.fetchall())
		print("\n---------------------------------------------------------------\n")
		print("Client ID:\t\t" + col2 + str(rows[0][2]) + rs.all)
		print("Client Name:\t\t" + col1 + str(rows[0][4]) + rs.all)
		print("Client Status:\t\t" + col1 + str(rows[0][3]) + rs.all)
		print("Adversite URL:\t\t" + col1 + str(rows[0][5]) + rs.all)
		print("Segment:\t\t" + col1 + str(rows[0][12]) + rs.all)
		print("\n")
		print("Corp ID:\t\t" + col1 + str(rows[0][0]) + rs.all)
		print("Corp Account:\t\t" + col1 + str(rows[0][1]) + rs.all)
		print("YoTrack Short:\t\t" + col1 + str(rows[0][11]) + rs.all)
		print("Address:\t\t" + col1 + str(rows[0][6]) + " " + str(rows[0][7]) + ", " + str(rows[0][8]) + ", " + str(rows[0][9]) + " " + str(rows[0][10]) + rs.all)	
		print("WBN Account:\t\t" + col1 + str(rows[0][13]) + rs.all)
		print("SF Account ID:\t\t" + col1 + str(rows[0][14]) + rs.all)
		print("Account UUID:\t\t" + col1 + str(rows[0][15]) + rs.all)
		print("Theme Key:\t\t" + col1 + str(rows[0][16]) + rs.all)
	except:
		print("Cannot run DB query")
		exit()

	#All Account Domains
	retrieved_CID = str(rows[0][2])
	try:
		cur.execute("SELECT cd.domainname, case when cd.domainstatus = '3' then 'Client Owned' when cd.domainstatus = '1' then 'Purchased' when cd.domainstatus = '0' then 'Desired' when cd.domainstatus = '2' then 'Pending' when cd.domainstatus = '7' then 'Custom' end as domainstatus, cd.registrarwebsite, case when cdc.domaintype = '0' then 'Advertising' when cdc.domaintype = '1' then 'Personal' when cdc.domaintype = '3' then 'OneSite' end as domaintype, case when cdc.sitetype = '0' then 'CMS2' when cdc.sitetype = '3' then 'CMS3' when cdc.sitetype = '1' then 'Proxy' end as sitetype, cdc.sslinstallstatus from control.client cc join control.domainname cd on cd.client_id = cc.id join control.domainnameconfiguration cdc on cdc.domainname_id = cd.id and cc.id in ({retrieved_CID})".format(**vars()))
		rows = list(cur.fetchall())
		domainnames=[]; domainstatuses=[]; registrarwebsites=[]; domaintypes=[]; sitetypes=[]; sslinstallstatuses=[]
		for row in rows:
			domainnames.append(row[0])
			domainstatuses.append(row[1])
			registrarwebsites.append(row[2])
			domaintypes.append(row[3])
			sitetypes.append(row[4])
			sslinstallstatuses.append(row[5])

		print("\n\nALL DOMAINS: (%d)\n-------------" % len(rows)) 
		for domainname, domainstatus, registrarwebsite, domaintype, sitetype, sslinstallstatus in zip(domainnames, domainstatuses, registrarwebsites, domaintypes, sitetypes, sslinstallstatuses):
			print("URL: " + col2 + domainname + rs.all + "\nStatus: " + col1 + str(domainstatus) + rs.all + " | Reg: " + col1 + str(registrarwebsite) + rs.all + " | DType: " + col1 + str(domaintype) + rs.all + " | SType: " + col1 + str(sitetype) + rs.all + " | SSL: " + col1 + str(sslinstallstatus) + rs.all)
			pingDomain(domainname)

	except:
		print("Cannot run DB query")
		exit()


	#All Account Phone Numbers 
	try:
		cur.execute("SELECT num.number, conf.routingnumber,ctc.primaryattribution, ctc.secondaryattribution,  ctc.usedestinationnumber,  conf.whisperon, conf.callrecordingon from control.calltrackingnumber num join control.calltrackingnumberconfiguration conf on conf.id = num.calltrackingnumberconfiguration_id left join control.ctcattributionconfig ctc on ctc.id = conf.attributionconfig_id where conf.client_id in ({retrieved_CID})".format(**vars()))
		rows = list(cur.fetchall())
		ctns=[]; routingnumbers=[]; pAttributions=[]; sAttributions=[]; showDests=[]; whispers=[]; callrecordings=[];
		for row in rows:
			ctns.append(row[0])
			routingnumbers.append(row[1])
			pAttributions.append(row[2])
			sAttributions.append(row[3])
			showDests.append(row[4])
			whispers.append(row[5])
			callrecordings.append(row[6])

		print("\nALL CTN NUMBERS: (%d)\n----------------" % len(rows)) 
		for ctn, routingnumber, pAttribution, sAttribution, showDest, whisper, callrecording in zip(ctns, routingnumbers, pAttributions, sAttributions, showDests, whispers, callrecordings):
			print("CTN: " + col2 + str(ctn) + rs.all + " | Rt: " + col1 + str(routingnumber) + rs.all + " | pA: " + col1 + str(pAttribution) + rs.all + " | sA: " + col1 + str(sAttribution) + rs.all + " | sDest: " + col1 + str(showDest)+ rs.all + " | Whpr: " + col1 + str(whisper) + rs.all + " | Rec: " + col1 + str(callrecording) + rs.all)

		cur.close()
	except:
		print("Cannot run DB query")
		exit()

	print("\n--------------------------------------------------------------")
	conn.close

# Domain Search
def searchDomain(domain_input):
	try:
		conn=psycopg2.connect( host="coredb2.prod.yodle.com", user=mySetup.natpalDbUsername, password=mySetup.natpalDbPassword, dbname="natpal")
	except:
		print("I am unable to connect to the database.")
	cur = conn.cursor()

	try:
		cur.execute("SELECT cd.domainname, cc.id, cc.status, cc.name, case when cd.domainstatus = '3' then 'Client Owned' when cd.domainstatus = '1' then 'Purchased' when cd.domainstatus = '0' then 'Desired' when cd.domainstatus = '2' then 'Pending' when cd.domainstatus = '7' then 'Custom' end as domainstatus, cd.registrarwebsite, case when cdc.domaintype = '0' then 'Advertising' when cdc.domaintype = '1' then 'Personal' when cdc.domaintype = '3' then 'OneSite' end as domaintype, case when cdc.sitetype = '0' then 'CMS2' when cdc.sitetype = '3' then 'CMS3' when cdc.sitetype = '1' then 'Proxy' end as sitetype, cdc.sslinstallstatus from control.domainname cd left join control.domainnameconfiguration cdc on cdc.domainname_id = cd.id left join control.client cc on cc.id = cd.client_id where cd.domainname = '{domain_input}'".format(**vars()))
		rows = list(cur.fetchall())
		domains=[]; clientids=[]; clientstatuses=[]; clientnames=[];domainstatuses=[]; registrationwebsites=[]; domaintypes=[]; sitetypes=[]; ssls=[];
		for row in rows:
			domains.append(row[0])
			clientids.append(row[1])
			clientstatuses.append(row[2])
			clientnames.append(row[3])
			domainstatuses.append(row[4])
			registrationwebsites.append(row[5])
			domaintypes.append(row[6])
			sitetypes.append(row[7])
			ssls.append(row[8])

		print("\n--------------------------------------------------------------")
		for domain, clientid, clientstatus, clientname, domainstatus, registrationwebsite, domaintype, sitetype, ssl in zip(domains, clientids, clientstatuses, clientnames, domainstatuses, registrationwebsites, domaintypes, sitetypes, ssls):
			print("Domain: " + col2 + str(domain) + rs.all)
			print("clientid: " + col1 + str(clientid) + rs.all)
			print("Status: " + col1 + str(clientstatus) + rs.all)
			print("Client Name: " + col1 + str(clientname) + rs.all)
			print("Domain Status: " + col1 + str(domainstatus) + rs.all)
			print("Registrar: " + col1 + str(registrationwebsite) + rs.all)
			print("Domain Type: " + col1 + str(domaintype) + rs.all)
			print("Site Type: " + col1 + str(sitetype) + rs.all)
			print("SSL Status: " + col1 + str(ssl) + rs.all + "\n")

		cur.close()
	except:
		print("Cannot run DB query")

	conn.close
	pingDomain(domain)
	print("\n--------------------------------------------------------------")

# CTN Phone Search
def searchPhone(phone_input):
	try:
		conn=psycopg2.connect( host="coredb2.prod.yodle.com", user=mySetup.natpalDbUsername, password=mySetup.natpalDbPassword, dbname="natpal")
	except:
		print("I am unable to connect to the database.")
	cur = conn.cursor()

	try:
		cur.execute("SELECT num.number, conf.routingnumber, cc.id, cc.name, cc.status, corp.id, corp.name, conf.name, ctc.primaryattribution, ctc.secondaryattribution, ctc.detectionkey, ctc.detectionkeyvalue, ctc.usedestinationnumber,  conf.whisperon, conf.callrecordingon from control.calltrackingnumber num left join control.calltrackingnumberconfiguration conf on conf.id = num.calltrackingnumberconfiguration_id left join control.ctcattributionconfig ctc on ctc.id = conf.attributionconfig_id left join control.client cc on cc.id = conf.client_id left join control.franchisemasteraccount_client fma on fma.franchisechildren_id = cc.id left join control.corporate_relationship corp on corp.fma_id = fma.franchisemasteraccount_id where corp.id is not null and num.number = '{phone_input}'".format(**vars()))
		rows = list(cur.fetchall())
		phones=[]; routings=[]; clientids=[]; clientnames=[]; clientstatuses=[]; corpids=[]; corpnames=[]; phonenames=[]; pattrs=[]; sattrs=[]; detectionkeys=[]; detectionvalues=[]; usedests=[];  whispers=[]; recs=[]
		for row in rows:
			phones.append(row[0])
			routings.append(row[1])
			clientids.append(row[2])
			clientnames.append(row[3])
			clientstatuses.append(row[4])
			corpids.append(row[5])
			corpnames.append(row[6])
			phonenames.append(row[7])
			pattrs.append(row[8])
			sattrs.append(row[9])
			detectionkeys.append(row[10])
			detectionvalues.append(row[11])
			usedests.append(row[12])
			whispers.append(row[13])
			recs.append(row[14])


		print("\n--------------------------------------------------------------")
		for phone, routing, clientid, clientname, clientstatus, corpid, corpname, phonename, pattr, sattr, detectionkey, detectionvalue, usedest,  whisper, rec in zip(phones, routings, clientids, clientnames, clientstatuses, corpids, corpnames, phonenames, pattrs, sattrs, detectionkeys, detectionvalues, usedests,  whispers, recs):
			print("CTN: " + col2 + phone + rs.all + " | Rt: " + col1 + routing + rs.all + " | ClientID: " + col1 + str(clientid) + rs.all)
			print("Routing:\t\t" + col1 + routing + rs.all)
			print("Client ID:\t\t" + col1 + str(clientid) + rs.all)
			print("Client Name:\t\t" + col1 + clientname + rs.all)
			print("Client Status:\t\t" + col1 + clientstatus + rs.all)
			print("\n")
			print("Corp ID:\t\t" + col1 + str(corpid) + rs.all)
			print("Corp Name:\t\t" + col1 + corpname + rs.all)
			print("\n")
			print("CTN Desc:\t\t" + col1 + phonename + rs.all)
			print("Primary Attr:\t\t" + col1 + str(pattr) + rs.all)
			print("Secondary Attr:\t\t" + col1 + str(sattr) + rs.all)
			print("Detection Key:\t\t" + col1 + str(detectionkey) + rs.all)
			print("Detection Val:\t\t" + col1 + str(detectionvalue) + rs.all)
			print("Use Dest:\t\t" + col1 + str(usedest) + rs.all)
			print("Whisper:\t\t" + col1 + str(whisper) + rs.all)
			print("Recording:\t\t" + col1 + str(rec) + rs.all)

		cur.close()
	except:
		print("Cannot run DB query")

	print("\n--------------------------------------------------------------")
	conn.close


def pingDomain(url):
	#url = "speedprobostonmetrowest.com"
	if "http" in url:
		url = url
	else:
		url = 'http://' + url
	try:
		r = requests.get(url)

		if len(r.history) > 0:
			chain = ""
			code = r.history[0].status_code
			initial_url = r.history[0].url
			final_url = r.url
			final_code = r.status_code
			for resp in r.history:
				chain += resp.url + " | "
			
			list = tldextract.extract(final_url)
			list_init = tldextract.extract(initial_url)
			final_domain = list.domain + '.' + list.suffix
			initial_domain = list_init.domain + '.' + list.suffix
			
			for z in dns.resolver.query(initial_domain, 'A'):
				initial_url_ip = z.to_text()
			for b in dns.resolver.query(initial_domain, 'NS'):
				initial_url_ns = b.to_text()

			for x in dns.resolver.query(final_domain, 'A'):
				url_ip = x.to_text()
			for y in dns.resolver.query(final_domain, 'NS'):
				url_ns = y.to_text()

			print("Initial HTTP Code:" + col1 + str(code) + rs.all)
			print("Initial URL IP: " + col1 + initial_url_ip + rs.all)
			print("Initial URL NS: " + col1 + initial_url_ns + rs.all)
			print("Redirects: " + col1 + str(len(r.history)) + rs.all)
			#print("Chain: " + chain)
			print("Final URL: " + col1 + final_url + rs.all)
			print("Final HTTP Code: " + col1 + str(final_code) + rs.all)
			print("Final URL IP: " + col1 + url_ip + rs.all)
			print("Final URL NS: " + col1 + url_ns + rs.all + "\n")
		else:
			final_url = r.url
			final_code = r.status_code
			list = tldextract.extract(final_url)
			final_domain = list.domain + '.' + list.suffix
			for x in dns.resolver.query(final_domain, 'A'):
				url_ip = x.to_text()
			for y in dns.resolver.query(final_domain, 'NS'):
				url_ns = y.to_text()			

			print("Redirects: " + str(len(r.history)))
			#print("Chain: " + chain)
			print("Final URL: " + final_url)
			print("Final HTTP Code: " + str(final_code))
			print("Final URL IP: " + url_ip)
			print("Final URL NS: " + url_ns + "\n")

	except requests.ConnectionError:
		print("Error: Domain not responding\n")

# Search Local Account
def searchAccount(name_query, name_status):
	try:
		conn=psycopg2.connect( host="coredb2.prod.yodle.com", user=mySetup.natpalDbUsername, password=mySetup.natpalDbPassword, dbname="natpal")
	except:
		print("I am unable to connect to the database.")
	cur = conn.cursor()

	try:
		cur.execute("SELECT cc.id, cc.name, cc.status from control.client cc where cc.name ilike '%{name_query}%' {name_status} order by cc.status".format(**vars()))
		rows = list(cur.fetchall())
		ccids=[]; ccnames=[]; ccstatuses=[]
		for row in rows:
			ccids.append(row[0])
			ccnames.append(row[1])
			ccstatuses.append(row[2])


		print("\n--------------------------------------------------------------")
		print("ClientID | Status | Client Name")
		for ccid, ccname, ccstatus in zip(ccids, ccnames, ccstatuses):
			print(col1 + str(ccid) + rs.all + " | " + col1 + ccstatus + rs.all + " | " + col1 + ccname + rs.all)

		print("\nNumber of accounts found: " + col1 + str(len(rows)) + rs.all)
		cur.close()
	except:
		print("Cannot run DB query")

	print("\n--------------------------------------------------------------")
	conn.close


# Corporate relationships by revenue
def corpRevenue(start_date, end_date):
	try:
		conn=psycopg2.connect( host="coredb2.prod.yodle.com", user=mySetup.natpalDbUsername, password=mySetup.natpalDbPassword, dbname="natpal")
	except:
		print("I am unable to connect to the database.")
	cur = conn.cursor()

	try:
		print("Pulling revenue data. Please wait...")
		cur.execute("SELECT corp.id, corp.name, round(sum(ili.amount)) as monthly_revenue from control.invoice i join control.invoicetransaction it on it.invoice_id=i.id join control.invoicelineitem ili on ili.invoice_id=i.id and ili.transaction_id=it.id join control.chargeableentity ce on ce.id=i.chargeableentity_id join control.franchisemasteraccount_client fma on fma.franchisechildren_id = ce.client_id join control.corporate_relationship corp on corp.fma_id = fma.franchisemasteraccount_id where it.transdate >= '{start_date}' and it.transdate < '{end_date}' and client_id in (select cc.id from control.client cc join control.franchisemasteraccount_client fma on fma.franchisechildren_id = cc.id join control.corporate_relationship corp on corp.fma_id = fma.franchisemasteraccount_id where cc.status = 'LIVE') group by corp.id order by monthly_revenue desc".format(**vars()))
		rows = list(cur.fetchall())
		corpids = []; corpnames = []; corprevs = []; corprev_sum = 0; indexnum = 0
		for row in rows:
			corpids.append(row[0])
			corpnames.append(row[1])
			corprevs.append(row[2])


		print("\n--------------------------------------------------------------")
		print("# | Corp ID | Revenue | Corp Name")
		for corpid, corpname, corprev in zip(corpids, corpnames, corprevs):
			corprev_sum = corprev_sum + corprev
			corprev = '{:,.0f}'.format(corprev)
			indexnum = indexnum + 1
			print("%s | %s | $%s | %s" % (indexnum, corpid, corprev, corpname))

		print("\nNumber of corporate accounts found: " + col1 + str(len(rows)) + rs.all)
		print("Total amount of monthly revenue: " + col1 + '${:,.2f}'.format(corprev_sum) + rs.all)
		cur.close()
	except:
		print("Cannot run DB query")

	print("\n--------------------------------------------------------------")
	conn.close


# Corporate Account Lookup
def corpAccountLookup(corp_identifier):
	try:
		conn=psycopg2.connect( host="coredb2.prod.yodle.com", user=mySetup.natpalDbUsername, password=mySetup.natpalDbPassword, dbname="natpal")
	except:
		print("I am unable to connect to the database.")
	cur = conn.cursor()

	#Main Account Info
	try:
		cur.execute("SELECT corp.id, corp.name, corp.fma_id, short_name, count(fma.franchisechildren_id) from control.corporate_relationship corp join control.franchisemasteraccount_client fma on fma.franchisemasteraccount_id = corp.fma_id join control.client cc on cc.id = fma.franchisechildren_id where cc.status = 'LIVE' and {corp_identifier} group by corp.id, corp.name, corp.fma_id, corp.short_name".format(**vars()))
		rows = list(cur.fetchall())
		corpids=[]; corpnames=[]; corpfmas=[]; corpshortnames=[];corplocations=[]
		for row in rows:
			corpids.append(row[0])
			corpnames.append(row[1])
			corpfmas.append(row[2])
			corpshortnames.append(row[3])
			corplocations.append(row[4])

		for corpid, corpname, corpfma, corpshortname, corplocation in zip(corpids, corpnames, corpfmas, corpshortnames, corplocations):
			print("\n---------------------------------------------------------------\n")
			print("Corporate ID:\t\t" + col2 + str(corpid) + rs.all)
			print("Corporate Name:\t\t" + col1 + str(corpname) + rs.all)
			print("Corp FMA ID:\t\t" + col1 + str(corpfma) + rs.all)
			print("yoTrack Shortname:\t" + col1 + str(corpshortname) + rs.all)
			print("Num of LIVE locations:\t" + col1 + str(corplocation) + rs.all + "\n")

			try:
				#Pulling revenue for this specific relationship
				cur.execute("SELECT round(sum(ili.amount)) as monthly_revenue from control.invoice i join control.invoicetransaction it on it.invoice_id=i.id join control.invoicelineitem ili on ili.invoice_id=i.id and ili.transaction_id=it.id join control.chargeableentity ce on ce.id=i.chargeableentity_id where it.transdate >= '2018.09.01' and it.transdate <= '2018.09.30' and client_id in (select cc.id from control.client cc join control.franchisemasteraccount_client fma on fma.franchisechildren_id = cc.id join control.corporate_relationship corp on corp.fma_id = fma.franchisemasteraccount_id where corp.id = {corpid})".format(**vars()))
				rows = list(cur.fetchall())
				print("Last Month Revenue:\t" + col1 + str('${:,.2f}'.format(rows[0][0])) + rs.all)
				print("\n")
			except:
				print("Revenue couldn't be retrieved\n")
			#Pulling list individual of individual accounts for this relationship
			print("Client IDs:")
			cur.execute("SELECT fma.franchisechildren_id from control.corporate_relationship corp join control.franchisemasteraccount_client fma on fma.franchisemasteraccount_id = corp.fma_id join control.client cc on cc.id = fma.franchisechildren_id where cc.status = 'LIVE' and corp.id = {corpid}".format(**vars()))
			rows = list(cur.fetchall())
			str1 = ''.join(str(e) for e in rows)
			str1 = str1.replace("(", ""); str1 = str1.replace(")",""); str1 = str1.replace(",", " ")
			print(col1 + str1 + rs.all)
		
			
	except:
		print("Cannot run DB query")

	print("\n--------------------------------------------------------------")
	conn.close





# Command Argument Choices
if (len(sys.argv) > 1 and sys.argv[1] == "-l"):
	order = "count desc"
	name_search = ""

elif (len(sys.argv) > 1 and sys.argv[1] == "-n"):
	order = "corp.name"
	name_search = ""

elif (len(sys.argv) > 1 and sys.argv[1] == "-c"):
	corp_identifier = sys.argv[2]
	if (corp_identifier.isdigit()):
		corp_identifier_final = ("corp.id = %s" % corp_identifier)
		corpAccountLookup(corp_identifier_final)
		exit()
	else:
		corp_identifier_final = ("corp.name ilike '%" + corp_identifier + "%'")
		corpAccountLookup(corp_identifier_final)
		exit()

elif (len(sys.argv) > 1 and sys.argv[1] == "-r"):
	if len(sys.argv) == 4:
		start_date = sys.argv[2] 
		end_date = sys.argv[3]
		corpRevenue(start_date, end_date)
		exit()
	else:
		print("\nFollow example: 'show -r 2018.09.01 2018.09.30'\n")
		exit()

elif (len(sys.argv) > 2 and sys.argv[1] == "-sc"):
	order = "corp.name"
	name_search = ("and corp.name ilike '%" + sys.argv[2] + "%'")

elif (len(sys.argv) > 2 and sys.argv[1] == "-sa"):
	name_search = sys.argv[2]
	if len(sys.argv) == 3:
		name_status = ""
	else:
		name_status = "and cc.status = '%s'" % sys.argv[3].upper()

	print(name_search, name_status)
	searchAccount(name_search, name_status)
	exit()

elif (len(sys.argv) > 2 and sys.argv[1] == "-sd"):
	domain_input = sys.argv[2].lower()
	searchDomain(domain_input)
	exit()

elif (len(sys.argv) > 2 and sys.argv[1] == "-sp"):
	phone_input = sys.argv[2]
	phone_input = phone_input.replace("-", "")
	phone_input = phone_input.replace(".", "")
	phone_input = phone_input.replace(" ", "")
	phone_input = phone_input.replace("(", "")
	phone_input = phone_input.replace(")", "")
	searchPhone(phone_input)
	exit()

elif (len(sys.argv) > 2 and sys.argv[1] == "-m"):
	corp_identifier_input = sys.argv[2]
	word = corp_identifier_input.isalpha()
	num = corp_identifier_input.isdigit()
	if word:
		corp_input_final = ("where cc.status='LIVE' and corp.name ilike '%" + corp_identifier_input +"%'")
		print(corp_input_final)
		microSites(corp_input_final)
		exit()
	if num:
		corp_input_final = ("where cc.status='LIVE' and corp.id = '%s'" % corp_identifier_input)
		microSites(corp_input_final)
		exit()

elif (len(sys.argv) > 2 and sys.argv[1] == "-a"):
	loc_account_input = sys.argv[2]
	if "." in loc_account_input:
		loc_input_final = ("cd.domainname = '%s'" % loc_account_input.lower())
		localAccountLookup(loc_input_final)
		exit()
	elif (loc_account_input.isdigit()):
		loc_input_final = ("cc.id in (%s)" % loc_account_input)
		localAccountLookup(loc_input_final)
		exit()
#	else:
#		print("Michal")
#		loc_input_final = ("cc.name ilike '%" + loc_account_input+"%'")
#		localAccountLookup(loc_input_final)
#		exit()
	exit()

else:
	print("\n---HELP----------------------------------------------------------\n")
	print(col1 + "show" + rs.all + "   (see help)\n")
	print(col2 + "CORPORATE LEVEL:" + rs.all)
	print(col1 + "show -l" + rs.all + "    (Show all LIVE corp accounts in # of locations order)")
	print(col1 + "show -n" + rs.all + " (Show all LIVE corp accounts in alphabetical order)")
	print(col1 + "show -c <corp ID or corp name>" + rs.all +"   (Show corporate account info)")
	print(col1 + "show -r <start date> <end date>"+rs.all+"  (Show all LIVE corp accounts in revenue order) ie: 'show -r 2018.09.01 2018.09.30'")
	print(col1 + "show -m <corp ID or corp Name>" + rs.all + "   (List accounts of given corp ID or corp Name)\n\n")
	print(col2 + "ACCOUNT LEVEL:" + rs.all)
	print(col1 + "show -a <account ID or domain>" + rs.all +"    (Local account info)")
	print(col2 + "\n\nSEARCH:" + rs.all)
	print(col1 + "show -sc <corp name>" + rs.all + "    (Search by corporate name)")
	print(col1 + "show -sa <account name> <optional: account status>" + rs.all + "   (Search by account name)")
	print(col1 + "show -sd <domain>" + rs.all + "    (Search Yodle Live by domain)")
	print(col1 + "show -sp <phone ctn>"+ rs.all + "   (Search Yodle Live by phone CTN)")
	print("\n")
	exit()


#Connecting to Postgres Natpal DB to pull list of accounts
try:
	conn=psycopg2.connect( host="coredb2.prod.yodle.com", user=mySetup.natpalDbUsername, password=mySetup.natpalDbPassword, dbname="natpal")
except:
	print("I am unable to connect to the database.")
cur = conn.cursor()
try:
	cur.execute("SELECT corp.id, corp.name, count(corp.id) from control.corporate_relationship corp join control.franchisemasteraccount_client fma on corp.fma_id = fma.franchisemasteraccount_id join control.client cc on fma.franchisechildren_id = cc.id where cc.status = 'LIVE' {name_search} group by corp.id, corp.name, corp.name, corp.fma_id order by {order}".format(**vars()))
	rows = list(cur.fetchall())
	corpIds = []; corpNames = []; locationCounts = []
	for row in rows:
		corpIds.append(row[0])
		corpNames.append(row[1])
		locationCounts.append(row[2])

	cur.close()
except:
	print("Cannot run DB query")

print("-----------------------------------------------------\nCorpID\t# Of Loc\tCorpName\n")
locationSum = 0
for corpId, corpName, locationCount in zip(corpIds, corpNames, locationCounts):
	locationSum += locationCount
	print(str(corpId) + "\t" + str(locationCount) + "\t" + corpName)

print("\nAll LIVE locations number: " + str(locationSum))
print("-----------------------------------------------------")

conn.close



