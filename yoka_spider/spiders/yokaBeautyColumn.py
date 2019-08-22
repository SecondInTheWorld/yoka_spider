# -*- coding: utf-8 -*-
import scrapy


class YokabeautycolumnSpider(scrapy.Spider):
    name = 'yokaBeautyColumn'
    allowed_domains = ['yoka.com']
    start_urls = ['http://yoka.com/']

    def parse(self, response):
        pass
