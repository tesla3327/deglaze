import scrapy
from scrapy.crawler import CrawlerProcess
from deglaze_scraper.spiders.google_spider import GoogleSpider

process = CrawlerProcess()

process.crawl(GoogleSpider, 'search+terms')
process.start()
