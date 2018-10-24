# -*- coding: utf-8 -*-
import scrapy
from scrapy.spiders import SitemapSpider

class Sitemapchecker(SitemapSpider):
	name = 'sitemapSpider'
	f = open("sitemapspider_url_list.txt")
#	sitemap_urls = ['http://www.affordabledentures.com/sitemap.xml', 'https://web.com/sitemap.xml']
	sitemap_urls = [url.strip() for url in f.readlines()]
	handle_httpstatus_list = [400,404,403,500,503,505]
	f.close()

	def parse(self, response):
		web_url = response.url
		web_status = response.status
		if web_status == 200:
			print(web_status)
		else:
			print('nie przeszlo')

		yield {
			'http response' : response.status,
			'url' : response.url,
			'referrer' : response.request.headers.get('Referer', None),
			'title': response.css("title ::text").extract_first(),
			'meta desc' : response.xpath("//meta[@name='description']/@content").extract(),
		}
		print(web_status, web_url)
	#!/usr/bin/env python

