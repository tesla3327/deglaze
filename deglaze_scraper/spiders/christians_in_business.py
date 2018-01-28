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
    #   print "Handling search disclaimer"

    #   yield FormRequest(
    #       'http://www.christiansinbusiness.com/search-disclaimer',
    #       formdata={"iAgree": "true"},
    #       callback=self.start_scraping,
    #       dont_filter=True
    #   )

    def clean_str_arr(self, arr):
        return filter(
            lambda str: str != '',
            map(
                lambda str: str.strip(),
                arr
            )
        )

    def start_scraping(self, response):
        print "Starting to scrape now"
        print response.headers

        yield Request(
            # 'http://www.christiansinbusiness.com/search?keyword=&location=&pageSize=100',
            # 'http://www.christiansinbusiness.com/business/47979/guarantee-real-estate---patrick-kim',
            'http://www.christiansinbusiness.com/business/43431/mccoy-blossom-funeral-home---moscow-mills',
            cookies={"BusinessSearchAgree": "True"},
            callback=self.parse_company_page,
            dont_filter=True
        )

    def parse_search_results(self, response):
        print 'Scraping: {}'.format(response.url)
        print

        companyUrls = response.xpath("//a[contains(text(),'Details')]/@href")
        for url in companyUrls:
            print url.extract()

    def parse_company_page(self, response):
        print 'Scraping company: {}'.format(response.url)

        company = {}

        company['company_name'] = response.xpath('//h2[@class="page-title"]/a/text()').extract()[0]

        context = response.xpath('//div[@class="agent"]')
        address_text = self.clean_str_arr(context.xpath('.//address/text()').extract())

        company['address'] = address_text[0]
        company['church'] = address_text[1]

        context = response.xpath('//div[@class="agent"]//div[@class="agent-contacts clearfix"]')
        company['url'] = context.xpath('./a[text()="Visit our website"]/@href').extract()[0].lower()
        social_media = context.xpath('./div[@class="social-media"]//li/a/@href').extract()
        company['social_media'] = ", ".join(social_media).lower()

        info_block_text = self.clean_str_arr(context.xpath('./div[@class="info-bar-block"]//text()').extract())

        company['contact_name'] = info_block_text[2]
        company['contact_title'] = info_block_text[4]

        company['contact_email'] = context.xpath('./a[text() = "Contact Us"]/@href').extract()[0].split(':')[1].lower()

        print company











