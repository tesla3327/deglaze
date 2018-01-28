import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from spiders.email_spider import EmailSpider
import logging
import csv

# Get the starting URLs we want to get emails from
list_of_start_urls = []
with open('websites.csv') as csvfile:
    readCSV = csv.reader(csvfile, delimiter=',')
    for row in readCSV:
        list_of_start_urls.append(row[0])

print 'Scraping {} websites for emails.\n\n'.format(len(list_of_start_urls))

# Get our settings
settings = get_project_settings()
settings.set('LOG_LEVEL', 'ERROR')

process = CrawlerProcess(settings)
process.crawl(EmailSpider, list_of_start_urls)
process.start()