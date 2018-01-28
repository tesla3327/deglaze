from scrapy import Spider, Request
import re
import urllib
from urlparse import urlparse

class SheperdsGuide(Spider):
    name = 'shepherds_guide'
    regex = r'WebsiteUrl%3D([^&]*)'
    search_url = 'https://www.google.ca/search?q=site:www.shepherdsguide.ca+website&num=100&start={}'
    max_results = 100

    def start_requests(self):
        for offset in range(0, self.max_results, 100):
            yield Request(self.search_url.format(offset))

    def parse(self, response):
        print 'Parsing: {}'.format(response.url)

        results = response.css('.r a::attr(href)')
        for link in results:
            href = link.extract()
            urlEncoded = re.search(self.regex, href).groups(1)
            url = urllib.unquote(urlEncoded).decode('utf8')
            hostname = urlparse(url).netloc
            print hostname
            yield { 'hostname': hostname }