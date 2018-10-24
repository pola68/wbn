import requests
import dns.resolver
import tldextract
import time



def get_status_code(url):
	if "http" in url:
		url = url + 'sitemap.xml'
	else:
		url = 'http://' + url + 'sitemap.xml'
	
	try:
		r = requests.get(url)
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


			return str(code) + ',' + str(len(r.history)) + ',' + chain + ',' + final_url + ',' + str(final_code)
		else:
			final_url = r.url
			final_code = r.status_code
			list = tldextract.extract(final_url)
			final_domain = list.domain + '.' + list.suffix

			
			return str(r.status_code) + ',,,' + final_url + ',' + str(final_code)
	except requests.ConnectionError:
		print("Error: failed to connect.")
		return '0,0,0,0,0'

timestr = time.strftime("%Y-%m-%d___%H-%M-%S")
input_file = 'urls_to_be_checked.txt'
output_file = 'output/domain-checkers-output-' + timestr + '.csv'

with open(output_file, 'w') as o_file:
	o_file.write('URL,Status,Number of redirects,Redirect Chain,Final URL,Final URL Status\n')
	f = open(input_file, "r")
	lines = f.read().splitlines()
	for line in lines:
		code = get_status_code(line)
		o_file.write(line + "," + str(code) + ",\n")
	f.close()








"""
#--Pull all NS records for given domain name

from dns.resolver import dns
name_server = '8.8.8.8' #Google's DNS server
ADDITIONAL_RDCLASS = 65535
request = dns.message.make_query('affordabledentures.com', dns.rdatatype.ANY)
request.flags |= dns.flags.AD
request.find_rrset(request.additional, dns.name.root, ADDITIONAL_RDCLASS,
                       dns.rdatatype.OPT, create=True, force_unique=True)       
response = dns.query.udp(request, name_server)
print(response)

"""
#-------------------------------------------------

"""

import requests

response = requests.get('http://google.com')
if response.history:
	print ("Request was redirected")
	for resp in response.history:
		print (resp.status_code, resp.url)
	print ("Final destination:")
	print (response.status_code, response.url)

else:
	print ("Request was not redirected")

"""
