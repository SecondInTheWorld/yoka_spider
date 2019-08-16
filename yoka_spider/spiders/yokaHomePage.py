# -*- coding: utf-8 -*-
import scrapy


class YokahomepageSpider(scrapy.Spider):
    name = 'yokaHomePage'
    allowed_domains = ['yoka.com']
    start_urls = ['http://yoka.com/']

    def parse(self, response):
        pass
