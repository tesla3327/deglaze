from scrapy import Spider, Request
import re
import urllib
from urlparse import urlparse

class SheperdsGuide(Spider):
    name = 'shepherds_guide2'
    regex = r'WebsiteUrl=([^&]*)'
    search_url = 'https://www.shepherdsguide.ca/master-categories.php?pub={}'
    download_delay = 1

    def start_requests(self):
        yield Request('https://www.shepherdsguide.ca/search.php?search=Auto%20Service%20%26%20Repair&pub_id=9', callback=self.parse_sub_category)
        # for pub in range(2, 4):
        #     yield Request(self.search_url.format(pub))

    def parse(self, response):
        print 'Parsing: {}'.format(response.url)

        main_categories = response.css('#categoriesPage a::attr(href)')
        for link in main_categories:
            href = link.extract()

            # Figure out how to parse this link
            if "search" in href:
                parse = self.parse_sub_category
            else:
                parse = self.parse

            yield Request(response.urljoin(href), callback=parse)

    def parse_sub_category(self, response):
        print 'Parsing subcategory: {}'.format(response.url)

        links = response.css('div.searchResult a')
        for link in links.css('::attr(href)'):
            href = link.extract()

            search = re.search(self.regex, href)

            if search:
                hostname = search.groups(1)[0]
                yield { 'hostname': hostname }

