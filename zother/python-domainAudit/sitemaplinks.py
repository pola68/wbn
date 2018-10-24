import requests
import dns.resolver
import tldextract
import time



def get_status_code(url):
	try:
		r = requests.get('http://' + url + '/sitemap.xml')
		#r = requests.get(url)
		print("Processing " + url)


		if len(r.history) > 0:
			chain = ""
			code = r.history[0].status_code
			final_url = r.url
			for resp in r.history:
				chain += resp.url + " | "
			
			list = tldextract.extract(final_url)
			final_domain = list.domain + '.' + list.suffix
			for x in dns.resolver.query(final_domain, 'A'):
				url_ip = x.to_text()
			for y in dns.resolver.query(final_domain, 'NS'):
				url_ns = y.to_text()

			return str(code) + '\t' + str(len(r.history)) + '\t' + chain + '\t' + final_url + '\t' + url_ip + '\t' + url_ns
		else:
			final_url = r.url
			list = tldextract.extract(final_url)
			final_domain = list.domain + '.' + list.suffix
			for x in dns.resolver.query(final_domain, 'A'):
				url_ip = x.to_text()
			for y in dns.resolver.query(final_domain, 'NS'):
				url_ns = y.to_text()
			
			return str(r.status_code) + '\t\t\t' + final_url + '\t' + url_ip + '\t' + url_ns
	except requests.ConnectionError:
		print("Error: failed to connect.")
		return '0\t0\t0\t0\t0\t'

timestr = time.strftime("%Y-%m-%d___%H-%M-%S")
input_file = 'urls_to_be_checked.txt'
output_file = 'output-' + timestr + '.txt'

with open(output_file, 'w') as o_file:
	o_file.write('URL\tStatus\tNumber of redirects\tRedirect Chain\tFinal URL\tFinal URL IP\tFinal URL NS\t\n')
	f = open(input_file, "r")
	lines = f.read().splitlines()
	for line in lines:
		code = get_status_code(line)
		o_file.write(line + "\t" + str(code) + "\t\n")
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
