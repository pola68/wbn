import requests, dns.resolver, tldextract, time
from pydrive.drive import GoogleDrive
from pydrive.auth import GoogleAuth
gauth = GoogleAuth(); gauth.LocalWebserverAuth(); drive = GoogleDrive(gauth)


def get_status_code(url):
	if "http" in url:
		url = url
	else:
		url = 'http://' + url
	
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

g_file = drive.CreateFile({"parents": [{"kind": "drive#fileLink", "id": '19kzjQTNCnfJGwIGitpD2Z4tE91rLL_29'}], 'title': 'basicDomainDNScheck-'+timestr+'.xls', 'mimeType': 'application/vnd.openxmlformats-officedocument.wordprocessingml.document'}) 
g_content = ""

with open(output_file, 'w') as o_file:
	o_file.write('URL,Status,Number of redirects,Redirect Chain,Final URL,Final URL Status\n')
	g_content += ('URL,Status,Number of redirects,Redirect Chain,Final URL,Final URL Status\n')
	f = open(input_file, "r")
	lines = f.read().splitlines()
	for line in lines:
		code = get_status_code(line)
		o_file.write(line + "," + str(code) + ",\n")
		g_content += (line + "," + str(code) + ",\n")
	f.close()
	g_file.SetContentString(g_content)
	g_file.Upload({'convert' : True})







