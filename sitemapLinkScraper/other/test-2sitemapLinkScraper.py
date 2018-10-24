import requests
from bs4 import BeautifulSoup
import urllib.request
import lxml
import dns.resolver
import tldextract


inputfile = open("input_urls.txt")
urls = [url.strip() for url in inputfile.readlines()]

#urls = ['http://www.ckosouthbay.com/sitemap.xml','https://www.fourseasonssunrooms.com/sitemap.xml','https://www.fourseasonssunrooms.com/locations/college-point-ny/sitemap.xml','https://www.worldgym.com/sitemap.xml']

def extract_links(url):
    ''' Open an XML sitemap and find content wrapped in loc tags. '''

    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'lxml')
    links = [element.text for element in soup.findAll('loc')]

    return links

sitemap_urls = []
for url in urls:
    r = requests.get(url)
    status = r.status_code
    links = extract_links(url)
    sitemap_urls += links
    if requests.ConnectionError:
        print("ERRRR")
    else:
        print(str(status) + " " + url)



print('Found {:,} URLs in the sitemap'.format(len(sitemap_urls)))

with open('sitemap_urls.csv', 'w') as f:
    for url in sitemap_urls:
        f.write(url + '\n')

f.close

