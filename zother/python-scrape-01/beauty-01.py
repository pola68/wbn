import requests
from bs4 import BeautifulSoup



page_link = 'https://www.affordabledentures.com/office/mesquite/'
# this is the url that we've already determined is safe and legal to scrape from.

page_response = requests.get(page_link, timeout=5)

soup = BeautifulSoup(page_response.content, "html.parser")

img = soup.findAll("img")
title = soup.title.string
p = soup.findAll("p")
meta = soup.findAll('meta',attrs={'name':'description'})
#meta2 = soup.find_all('meta',attrs={'name':'generator'})
#clean = tag1.text.strip()

#for tags in soup.findAll('meta'):
#	print(tags.get('content'))


#print(img);
#print(title);
#print(p);
print(meta);
