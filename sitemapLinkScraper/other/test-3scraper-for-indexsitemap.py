import requests
from bs4 import BeautifulSoup

url = 'https://www.affordabledentures.com/sitemap-index.xml'
page = requests.get(url)
print('Loaded page with: %s' % page)

sitemap_index = BeautifulSoup(page.content, 'html.parser')
print('Created %s object' % type(sitemap_index))

urls = [element.text for element in sitemap_index.findAll('loc')]
print(urls)

def extract_links(url):
    ''' Open an XML sitemap and find content wrapped in loc tags. '''

    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    links = [element.text for element in soup.findAll('loc')]

    return links

sitemap_urls = []
for url in urls:
    links = extract_links(url)
    sitemap_urls += links

print('Found {:,} URLs in the sitemap'.format(len(sitemap_urls)))

with open('sitemap_urls.txt', 'w') as f:
    for url in sitemap_urls:
        f.write(url + '\n')

