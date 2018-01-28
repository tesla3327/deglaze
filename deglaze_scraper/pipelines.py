# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from scrapy.exceptions import DropItem

class DuplicateEmailsPipeline(object):

    def __init__(self):
        self.emails_seen = set()

    def process_item(self, item, spider):
        if item['email'] in self.emails_seen:
            raise DropItem("Duplicate email found: %s" % item)
        else:
            self.emails_seen.add(item['email'])
            return item