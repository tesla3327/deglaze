# -*- coding: utf-8 -*-
from scrapy import Spider, Request
from scrapy.http import FormRequest

class ChristiansInBusinessSpider(Spider):
    name = 'christians_in_business'
    allowed_domains = ['www.christiansinbusiness.com']
    start_urls = ['http://www.christiansinbusiness.com/']

    # Set a cookie to agree to terms and conditions
    def start_requests(self):
    	yield Request(
    		'http://www.christiansinbusiness.com/search',
    		cookies={'BusinessSearchAgree': 'True'},
    		callback=self.start_scraping,
    		dont_filter=True
    	)

    # def handle_search_disclaimer(self, response):
    # 	print "Handling search disclaimer"

    # 	yield FormRequest(
    # 		'http://www.christiansinbusiness.com/search-disclaimer',
    # 		formdata={"iAgree": "true"},
    # 		callback=self.start_scraping,
    # 		dont_filter=True
    # 	)

    def start_scraping(self, response):
    	print "Starting to scrape now"
    	print response.headers

    	yield Request(
    		# 'http://www.christiansinbusiness.com/search?keyword=&location=&pageSize=100',
    		'http://www.christiansinbusiness.com/business/47979/guarantee-real-estate---patrick-kim',
    		cookies={"BusinessSearchAgree": "True"},
    		callback=self.parse_company,
    		dont_filter=True
    	)

    def parse_search_results(self, response):
    	print 'Scraping: {}'.format(response.url)
    	print

    	companyUrls = response.xpath("//a[contains(text(),'Details')]/@href")
    	for url in companyUrls:
    		print url.extract()

  	def parse_company(self, response):
  		print 'Scraping company: {}'.format(response.url)

  		











