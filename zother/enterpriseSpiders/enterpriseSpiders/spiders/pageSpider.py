#--------------------------------------------------
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
import scrapy
import csv
import sys


class FirstSpider(CrawlSpider):
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
	#	url4 = ("Status: " + str(response.status) + " URL: " + response.url)
	#	allinfo = (str(response.url) + " " + str(response.css('h1::text').extract()))
		#print(allinfo)

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







#-------------------------------
"""
		for item in zip(web_stat,web_url,title,metadesc):
			zebrane = {
			'status' : item[0],
			'url' : item[1],
			'title' : item[2],
			'description' : item[3]
			}  	
			print(item)
			yield zebrane

"""


#----------------------------------------------
"""
import scrapy

from scrapy.spidermiddlewares.httperror import HttpError
from twisted.internet.error import DNSLookupError
from twisted.internet.error import TimeoutError, TCPTimedOutError

class ErrbackSpider(scrapy.Spider):
	name = "errback_example"
	start_urls = [
		"http://www.httpbin.org/",              # HTTP 200 expected
		"http://www.httpbin.org/status/404",    # Not found error
		"http://www.httpbin.org/status/500",    # server issue
		"http://www.httpbin.org:12345/",        # non-responding host, timeout expected
		"http://www.httphttpbinbin.org/",       # DNS error expected
	]

	def start_requests(self):
		for u in self.start_urls:
			yield scrapy.Request(u, callback=self.parse_httpbin,
				errback=self.errback_httpbin,
				dont_filter=True)

	def parse_httpbin(self, response):
		self.logger.info('Got successful response from {}'.format(response.url))
		print(response.url)

		def errback_httpbin(self, failure):
		# log all failures

			self.logger.error(repr(failure))

		# in case you want to do something special for some errors,
		# you may need the failure's type:

		if failure.check(HttpError):
			# these exceptions come from HttpError spider middleware
			# you can get the non-200 response

			response = failure.value.response
			self.logger.error('HttpError on %s', response.url)

		elif failure.check(DNSLookupError):
			# this is the original request
			request = failure.request
			self.logger.error('DNSLookupError on %s', request.url)

		elif failure.check(TimeoutError, TCPTimedOutError):
			request = failure.request
			self.logger.error('TimeoutError on %s', request.url)

		"""



#-----------------------------------------


"""
--------------------------------------------------
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
#from scrapy.items import PicItem
import scrapy


class FirstSpider(CrawlSpider):
	name = 'first'
	allowed_domains = ['www.dki-xpertrestoration.com','www.magiclanddental.com']
	start_urls = ['http://www.dki-xpertrestoration.com/','https://www.magiclanddental.com/']

	rules = [
		Rule(LinkExtractor(allow=['.*']), callback = 'parse_item', follow = True)

	]

	def parse_item(self, response):
	#	url4 = ("Status: " + str(response.status) + " URL: " + response.url)
	#	allinfo = (str(response.url) + " " + str(response.css('h1::text').extract()))
		#print(allinfo)

	#	url = "lalalala"
	#	status = "blue"
		title = response.css('title::text').extract()
		metadesc = response.xpath("//meta[@name='description']/@content").extract()
		web_stat = str(response.status)
		web_url = response.url
		
		print(title)

		for item in zip(web_stat,web_url,title,metadesc):
			zebrane = {
			'status' : item[0],
			'url' : item[1],
			'title' : item[2],
			'description' : item[3]
			}  	
			yield zebrane




#-----------------------------------------
"""

"""
import scrapy

class FirstSpider(scrapy.Spider):
	name = 'first'
	allowed_domains = ['www.reddit.com/r/gameofthrones/']
	start_urls = ['http://www.reddit.com/r/gameofthrones/']


	def parse(self, response):
		titles = response.css('.title.may-blank::text').extract()
		votes = response.css('.score.unvoted::text').extract()
		times = response.css('time::attr(title)').extract()
		comments = response.css('.comments::text').extract()

		#Give the extracted content row wise
		for item in zip(titles,votes,times,comments):
			scraped_info = {
			'title' : item[0],
			'vote' : item[1],
			'created_at' : item[2],
			'comments' : item[3],
			}

			yield scraped_info

"""