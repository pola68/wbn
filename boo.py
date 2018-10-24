#!/usr/bin/env python
import psycopg2, sys, requests, dns.resolver, tldextract, time
from sty import fg, bg, ef, rs, Rule, Render
#from termcolor import colored, cprint
sys.path.append('/tools')
import mySetup

url = "speedprobostonmetrowest.com"

if "http" in url:
	url = url
else:
	url = 'http://' + url




try:
	r = requests.get(url)
	print(fg.li_red + r.url + fg.rs)
	print(r.history[0].status_code)
	print(r.status_code)

except requests.ConnectionError:
	print("Error: failed to connect.\n")

print("Domain: " + r.url)
