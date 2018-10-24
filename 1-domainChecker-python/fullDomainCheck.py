import requests
import dns.resolver
import tldextract
import time



def get_status_code(url):
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
			for y in dns.resolver.query(final_domain, 'NS'):
				url_ns = y.to_text()
			
			return str(r.status_code) + ',,,' + final_url + ',' + str(final_code) + ',' + url_ip + ',' + url_ns
	except requests.ConnectionError:
		print("Error: failed to connect.")
		return '0,0,0,0,0,0,0'

timestr = time.strftime("%Y-%m-%d___%H-%M-%S")
input_file = 'urls_to_be_checked.txt'
output_file = 'output/domain-checkers-output-' + timestr + '.csv'

with open(output_file, 'w') as o_file:
	o_file.write('URL,Status,Number of redirects,Redirect Chain,Final URL,Final URL Status,Final URL IP,Final URL NS,\n')
	f = open(input_file, "r")
	lines = f.read().splitlines()
	for line in lines:
		code = get_status_code(line)
		o_file.write(line + "," + str(code) + ",\n")
	f.close()




