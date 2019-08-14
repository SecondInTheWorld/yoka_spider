# -*- coding: utf-8 -*-
import scrapy


class AaaSpider(scrapy.Spider):
    name = 'aaa'
    allowed_domains = ['yoka.com']
    start_urls = ['http://yoka.com/']

    def parse(self, response):
        pass
