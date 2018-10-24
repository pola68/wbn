#!/usr/bin/env python

# -*- coding: utf-8 -*-
import scrapy
from scrapy.spiders import SitemapSpider
from scrapy.crawler import CrawlerProcess
import dns.resolver
import tldextract
import time

class sitemapSpider(SitemapSpider):
	name = 'sitemapSpider'
	f = open("urls_list_sitemapspider.txt")
#	sitemap_urls = ['http://www.affordabledentures.com/sitemap.xml', 'https://web.com/sitemap.xml']
	sitemap_urls = [url.strip() for url in f.readlines()]
	handle_httpstatus_list = [400,404,403,500,503,505]
	f.close()

	def parse(self, response):
		web_url = response.url
		web_status = response.status


		yield {
			'http response' : response.status,
			'url' : response.url,
			'referrer' : response.request.headers.get('Referer', None),
			'title': response.css("title ::text").extract_first(),
			'meta desc' : response.xpath("//meta[@name='description']/@content").extract(),
		}
		print(web_status, web_url)

# --- it runs without project and saves in `output.csv` ---


timestr = time.strftime("%Y-%m-%d___%H-%M-%S")
c = CrawlerProcess({
    'USER_AGENT': 'Mozilla/5.0',

    # save in file as CSV, JSON or XML
    'FEED_FORMAT': 'csv',     # csv, json, xml
    'FEED_URI': 'output/sitemapSpider-' + timestr + '-output.csv', # 
})
c.crawl(sitemapSpider)
c.start()

