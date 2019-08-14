# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class YokaSpiderItem(scrapy.Item):
    # 网站名
    site_name = scrapy.Field()
    # 域名
    domain = scrapy.Field()
    # 域名地址
    domain_url = scrapy.Field()
    # 一级栏目名（模块名）
    first_title = scrapy.Field()
    first_title_url = scrapy.Field()
    # 二级栏目名
    second_title = scrapy.Field()
    second_title_url = scrapy.Field()
    # 栏目等级
    column_level = scrapy.Field()
    # 详情页标题
    title_detail = scrapy.Field()
    # 详情链接
    link_url = scrapy.Field()
    # 图片地址
    img_url = scrapy.Field()
    # 发布时间
    release_time = scrapy.Field()
    # 编辑者
    compiler = scrapy.Field()
    # 内容详情
    content_detail = scrapy.Field()
    # 来源于
    come_from = scrapy.Field()
    # 详情页图片地址
    detail_img_url = scrapy.Field()
    pass
