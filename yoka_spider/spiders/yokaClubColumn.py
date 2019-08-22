# -*- coding: utf-8 -*-
import scrapy


class YokaclubcolumnSpider(scrapy.Spider):
    name = 'yokaClubColumn'
    allowed_domains = ['yoka.com']
    start_urls = ['http://yoka.com/']

    def parse(self, response):
        pass
