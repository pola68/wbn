#--------------------------------------------------
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
import scrapy
import csv
import sys
from scrapy.crawler import CrawlerProcess
import time


class pageSpider(CrawlSpider):
	name = 'pageSpider'

	f = open("pagespider_url_list.txt")
	al = open("pagespider_allowed_list.txt")

#	allowed_domains = ['affordabledentures.com']
#	start_urls = ['https://www.affordabledentures.com/office/tracy/']
	allowed_domains = [url.strip() for url in al.readlines()]
	start_urls = [url.strip() for url in f.readlines()]
	handle_httpstatus_list = [400,404,403,500,503,505]
	f.close()
	al.close()
	

	rules = [
		Rule(LinkExtractor(allow=['.*']), callback = 'parse_item', follow = True)
	]

	def parse_item(self, response):
		self.logger.info('Parse function called on %s', response.url)

		title = response.css('title::text').extract()
		metadesc = response.xpath("//meta[@name='description']/@content").extract() 
		web_h11 = response.css('h1').extract()
#		web_h12 = response.css('h1')[1].extract()[1]
#		web_h13 = response.css('h1')[2].extract()
#		web_h21 = response.xpath("//h2")[0].extract()
#		web_h22 = response.xpath("//h2")[1].extract()
#		web_h23 = response.xpath("//h2")[2].extract()
		web_stat = str(response.status)
		web_url = response.url
		web_ref = response.request.headers.get('Referer', None)
#		test2 = response.css('.fees-wrap').extract()

		print(web_stat, web_url)

		yield {
		'status' : web_stat,
		'url' : web_url,
		'title' : title,
		'description' : metadesc,
		'h1-1' : web_h11,
#		'h1-2' : web_h12,
#		'h1-3' : web_h13,
		'referer' : web_ref
		}

timestr = time.strftime("%Y-%m-%d___%H-%M-%S")
c = CrawlerProcess({
    'USER_AGENT': 'Mozilla/5.0',

    # save in file as CSV, JSON or XML
    'FEED_FORMAT': 'csv',     # csv, json, xml
    'FEED_URI': 'output/pageSpider-' + timestr + '-output.csv', # 
})
c.crawl(pageSpider)
c.start()


