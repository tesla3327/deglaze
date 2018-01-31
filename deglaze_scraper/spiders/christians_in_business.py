# -*- coding: utf-8 -*-
from scrapy import Spider, Request
from scrapy.http import FormRequest

def acc(arr, index):
    if len(arr) >= index + 1:
        return arr[index]
    else:
        return ''

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

        for page in range(6, 21):
            yield Request(
                'http://www.christiansinbusiness.com/search?keyword=&location=&pageSize=100&pg={}'.format(page),
                cookies={"BusinessSearchAgree": "True"},
                callback=self.parse_search_results,
                dont_filter=True
            )

    def parse_search_results(self, response):
        print 'Scraping: {}'.format(response.url)
        print

        companyUrls = response.xpath("//a[contains(text(),'Details')]/@href")
        for url in companyUrls:
            yield Request(
                response.urljoin(url.extract()),
                cookies={"BusinessSearchAgree": "True"},
                callback=self.parse_company_page
            )

    def parse_company_page(self, response):
        print 'Scraping company: {}'.format(response.url)

        company = {}

        page_titles = response.xpath('//h2[@class="page-title"]/a/text()').extract()
        company['company_name'] = acc(page_titles, 0)

        context = response.xpath('//div[@class="agent"]')
        address_text = self.clean_str_arr(context.xpath('.//address/text()').extract())

        company['address'] = acc(address_text, 0)
        company['church'] = acc(address_text, 1)

        context = response.xpath('//div[@class="agent"]//div[@class="agent-contacts clearfix"]')
        company['url'] = acc(context.xpath('./a[text()="Visit our website"]/@href').extract(), 0).lower()

        social_media = context.xpath('./div[@class="social-media"]//li/a/@href').extract()
        company['social_media'] = ", ".join(social_media).lower()

        info_block_text = self.clean_str_arr(context.xpath('./div[@class="info-bar-block"]//text()').extract())

        company['contact_name'] = acc(info_block_text, 2)
        company['contact_title'] = acc(info_block_text, 4)

        unprocessed_email = acc(context.xpath('./a[text() = "Contact Us"]/@href').extract(), 0)
        company['contact_email'] = acc(unprocessed_email.split(':'), 1).lower()

        yield company











