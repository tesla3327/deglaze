import scrapy
from scrapy.spiders import Spider, Rule, Request
import urllib
from urlparse import urlparse
import re
import logging
from scrapy.utils.log import configure_logging

class EmailSpider(Spider):
    name = 'email_spider'
    email_regex = r'\b[\w.-]+?@\w+?\.\w+?\b'
    download_delay = 1
    custom_settings = {
        'ITEM_PIPELINES': {
            'deglaze_scraper.pipelines.DuplicateEmailsPipeline': 100,
        },
        'FEED_FORMAT': 'csv',
        'FEED_URI': 'emails.csv'
    }

    def __init__(self, list_of_start_urls=['https://clearchoiceautoglass.ca']):
        super(EmailSpider, self).__init__()
        self.list_of_start_urls = list_of_start_urls

    def start_requests(self):
        for url in self.list_of_start_urls:
            if not url.startswith('http'):
                url = 'http://www.' + url

            request = Request(url)
            request.meta['orig_domain'] = urlparse(url).netloc
            yield request


    def parse(self, response):
        print 'Parsing for emails: {}'.format(response.url)
        print response.meta['orig_domain']

        # Find any links
        links = response.css('a::attr(href)')

        for link in links:
            href = link.extract()

            # Follow if absolute path to current domain or relative path
            url = response.urljoin(href)
            if response.meta['orig_domain'] in url:
                request = Request(url)
                request.meta['orig_domain'] = response.meta['orig_domain']
                yield request

        # Parse out any emails
        hostname = urlparse(response.url).netloc
        pageAsText = response.body.decode(response.encoding)
        emails = re.findall(self.email_regex, pageAsText)
        print emails
        for email in emails:
            yield {
                'hostname': hostname.lower(),
                'email': email.lower()
            }