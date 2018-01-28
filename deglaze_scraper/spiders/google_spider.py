from scrapy import Spider, Request
import re
import urllib
from urlparse import urlparse

class GoogleSpider(Spider):
    name = 'google'
    regex = r'url\?q=([^&]*)&'

    def __init__(self, query):
        self.query = query

    def start_requests(self):
        yield Request('https://www.google.ca/search?q={}&num=100'.format(self.query))
        yield Request('https://www.google.ca/search?q={}&num=100&start=100'.format(self.query))
        yield Request('https://www.google.ca/search?q={}&num=100&start=200'.format(self.query))

    def parse(self, response):
        print 'Parsing: {}'.format(response.url)

        results = response.css('.r a::attr(href)')
        for link in results:
            href = link.extract()
            url = urllib.unquote(href).decode('utf8')
            hostname = urlparse(url).netloc
            yield { 'hostname': hostname }