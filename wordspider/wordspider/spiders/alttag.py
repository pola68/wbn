#!/usr/bin/env python

from io import StringIO
from functools import partial
from scrapy.http import Request
from scrapy.spiders import BaseSpider
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.item import Item
import csv

def find_all_substrings(string, sub):

	import re
	starts = [match.start() for match in re.finditer(re.escape(sub), string)]
	return starts

class WebsiteSpider(CrawlSpider):

	name = "alttag"

	f = open("wordspider_urls.csv")
	csv_f = csv.reader(f)
	start_urls = []
	allowed_domains = []
	for row in csv_f:
		start_urls.append(row[0])
		allowed_domains.append(row[1])
	f.close()



	#allowed_domains = ["cowsoforlando.com","www.fourseasonssunrooms.com"]
	#start_urls = ["https://www.cowsoforlando.com/","https://www.fourseasonssunrooms.com/"]
	rules = [Rule(LinkExtractor(), follow=True, callback="check_buzzwords")]

	crawl_count = 0
	words_found = 0                                 

	def check_buzzwords(self, response):

		self.__class__.crawl_count += 1

		crawl_count = self.__class__.crawl_count

		wordlist = [
			'<img',
			]

		url = response.url
		contenttype = response.headers.get("content-type", "").decode('utf-8').lower()
		data = response.body.decode('utf-8')

		for word in wordlist:
				substrings = find_all_substrings(data, word)
				for pos in substrings:
						ok = False
						if not ok:
								self.__class__.words_found += 1
								print(word + "," + url + ",")
		return Item()

	def _requests_to_follow(self, response):
		if getattr(response, "encoding", None) != None:
				return CrawlSpider._requests_to_follow(self, response)
		else:
				return []

