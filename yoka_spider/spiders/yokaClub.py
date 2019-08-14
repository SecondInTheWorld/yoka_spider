# -*- coding: utf-8 -*-
import datetime
import json
import logging
import math
from copy import deepcopy

import scrapy

from yoka_spider.items import YokaSpiderItem


class YokaclubSpider(scrapy.Spider):
    name = 'yokaClub'
    allowed_domains = ['yoka.com']

    def start_requests(self):
        try:
            # 第一版板块
            # 进行起始 url 的拼接
            url_list = {'http://www.yoka.com/club/': '时尚', 'http://beauty.yoka.com/': '美容',
                        'http://luxury.yoka.com/': '奢华',
                        'http://star.yoka.com/': '明星', 'http://life.yoka.com/': '乐活', 'http://www.yokamen.cn/': '男士',
                        'http://www.yoka.com/video/': '视频', 'http://www.yoka.com/z/': '独家',
                        'http://bbs.yoka.com/': '社区',
                        'http://brand.yoka.com/': '品牌'}
            # first_title = ['时尚', '美容', '奢华', '明星', '乐活', '男士', '视频', '独家', '社区', '品牌']
            self.nowData = str(datetime.datetime.now())[0:10]
            self.headers = {"Host": " www.yoka.com",
                            "User-Agent: Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv": "68.0) Gecko/20100101 Firefox/68.0",
                            "Accept": " text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
                            "Accept-Language": " zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2",
                            "Accept-Encoding": " gzip, deflate",
                            "Connection": " keep-alive"}
            for key, value in url_list.items():
                # 一级栏目
                item = YokaSpiderItem()
                # item = {}
                item['site_name'] = '优卡网'
                item['domain'] = 'www.yoka.com'
                item['domain_url'] = 'http://www.yoka.com/'
                item['first_title'] = '优卡网-首页-' + value
                item['first_title_url'] = key
                yield scrapy.Request(
                    method="GET",
                    url=key,
                    headers=self.headers,
                    callback=self.parse,
                    meta={'item': item}
                )
                print('时尚栏目数据抓取完成-----------------------------------')
                break
        except Exception as e:
            print(e)
            logging.info(e)

    def parse(self, response):
        """获取第二层栏目信息"""
        item = response.meta['item']
        # 获取第二层栏目url
        for aNode in response.xpath('//*[@id="p_nav_box_high"]/a'):
            # 二级栏目
            item['second_title'] = item['first_title'] + '-' + aNode.xpath('./text()').extract_first()
            item['second_title_url'] = aNode.xpath('./@href').extract_first()
            # print("item['second_title_url']", item['second_title_url'])
            yield scrapy.Request(
                method="GET",
                url=item['second_title_url'],
                callback=self.parse_info,
                meta={'item': deepcopy(item)}
            )
        pass

    def parse_info(self, response):
        """获取内页信息"""
        item = response.meta['item']
        # 获取有焦点栏详情标题等
        details_focus = response.xpath('//*[@id="fFocus"]/div/div[contains(@class,"item")]')
        if details_focus:
            for index, detail in enumerate(details_focus):
                # 栏目等级
                item['column_level'] = '一级栏目'
                # 详情标题
                item['title_detail'] = ' '.join([i.strip() for i in detail.xpath('./a/dl//text()').extract()])
                # 详情链接
                item['link_url'] = response.urljoin(detail.xpath('./a[1]/@href').extract_first())
                # print("item['link_url']", item['link_url'])
                # 图片url
                item['img_url'] = detail.xpath('./a/img/@src').extract_first()
                # 发布时间
                self.get_release_time(item)
                # print(item['release_time'])
                if item['link_url']:
                    yield scrapy.Request(
                        method="GET",
                        url=item['link_url'],
                        callback=self.parse_detail,
                        meta={'item': deepcopy(item)}
                    )
                pass
        else:
            with open('focus_kong.txt', 'a') as f:
                f.write(str(response.url) + '\n')

        # 获取box栏详情
        details_box = response.xpath('//div[contains(@class,"g-list")]')
        # details_box_last = response.xpath('//*[@id="loadMoreBox"]/div')
        # details_box.extend(details_box_last)
        if details_box:
            for detail in details_box:
                # print('title_detail', detail)
                # 栏目等级
                item['column_level'] = '--'
                # 详情
                item['title_detail'] = detail.xpath('./div[@class="tit"]/a/text()').extract_first()
                # 详情链接
                item['link_url'] = response.urljoin(detail.xpath('./div[@class="tit"]/a[1]/@href').extract_first())
                # print("item['link_url']---box", item['link_url'])
                # 图片url
                item['img_url'] = detail.xpath('./div[@class="img"]/a/img/@src').extract_first()
                # 发布时间
                self.get_release_time(item)
                if item['link_url']:
                    yield scrapy.Request(
                        method="GET",
                        url=item['link_url'],
                        callback=self.parse_detail,
                        meta={'item': deepcopy(item)}
                    )

        # 秀场类数据
        details_focus_show = response.xpath('//*[@id="fullImgBox"]/div[contains(@class, "full")]')
        if details_focus_show:
            # 焦点栏数据
            for index, detail in enumerate(details_focus_show):
                # 栏目等级
                item['column_level'] = '一级栏目'
                # 详情标题
                item['title_detail'] = detail.xpath('./a/text()').extract_first()
                # 详情链接
                item['link_url'] = response.urljoin(detail.xpath('./a/@href').extract_first())
                # print("item['link_url']", item['link_url'])
                # 图片url
                item['img_url'] = detail.xpath('./a/img/@src').extract_first()
                # 发布时间
                # release_time = response.xpath('/html/body/div/div/div[2]/div[1]/div/i/text()').extract_first()
                self.get_release_time(item)
                # print(item['release_time'])
                if item['link_url']:
                    yield scrapy.Request(
                        method="GET",
                        url=item['link_url'],
                        callback=self.parse_detail,
                        meta={'item': deepcopy(item)}
                    )
            # fashion栏数据
            details_box_show = response.xpath('//div[@class="lcn-1"]')
            if details_box_show:
                for detail in details_box_show:
                    # 栏目等级
                    item['column_level'] = '--'
                    # 详情标题
                    item['title_detail'] = detail.xpath('./dl/dd[1]/a/text()').extract_first()
                    # 详情链接
                    item['link_url'] = response.urljoin(detail.xpath('./dl/dd[1]/a/@href').extract_first())
                    # print("item['link_url']", item['link_url'])
                    # 图片url
                    item['img_url'] = detail.xpath('./dl/dt/a/img/@src').extract_first()
                    # 发布时间
                    self.get_release_time(item)
                    # print(item['release_time'])
                    if item['link_url']:
                        yield scrapy.Request(
                            method="GET",
                            url=item['link_url'],
                            callback=self.parse_detail,
                            meta={'item': deepcopy(item)}
                        )
            # 热门事件栏数据
            details_fashion_show = response.xpath('//*[@id="zIndexB"]')
            if details_fashion_show:
                for detail in details_fashion_show:
                    # 热门分类标题
                    hot_title = detail.xpath('./dl/dd[1]/a/text()').extract_first()
                    # print("hot_title", hot_title)
                    # if '巴黎' in hot_title:
                    # 详情链接
                    hot_url = response.urljoin(detail.xpath('./dl/dd[1]/a/@href').extract_first())
                    # print("hot_url", hot_url)
                    if hot_url:
                        yield scrapy.Request(
                            method="GET",
                            url=hot_url,
                            callback=self.parse_hot_detail,
                            meta={'item': deepcopy(item)}
                        )

    def parse_hot_detail(self, response):
        """热门栏目数据"""
        item = response.meta['item']
        hot_detail_list = response.xpath('//div[@class="filterResultList"]')
        if hot_detail_list:
            for detail in hot_detail_list:
                # 栏目等级
                item['column_level'] = '--'
                # 详情标题
                item['title_detail'] = detail.xpath('./ul/li/h3/a/text()').extract_first()
                # 详情链接
                item['link_url'] = response.urljoin(detail.xpath('/ul/li/div/a/@href').extract_first())
                # print("hot item['link_url']", item['link_url'])
                # 图片url
                item['img_url'] = detail.xpath('./ul/li/div/a/img/@src').extract_first()
                # 发布时间
                # release_time = response.xpath('/html/body/div/div/div[2]/div[1]/div/i/text()').extract_first()
                self.get_release_time(item)
                yield scrapy.Request(
                    method="GET",
                    url=item['link_url'],
                    callback=self.parse_detail,
                    meta={'item': deepcopy(item)}
                )
        pass

    def parse_detail(self, response):
        """获取详情内容和发布时间"""
        # item = YokaSpiderItem()
        item = response.meta['item']
        auther = response.xpath('/html/body/div/div/div[2]/div/dl/dd/i/text()').extract_first()
        if auther:
            # 编辑者
            item['compiler'] = auther
            # 来源于
            from_text = response.xpath('//div[@class="infoTime"]/div/a/text()').extract_first()
            if not from_text:
                from_text = response.xpath('//li[contains(text(),"来源于：")]/a/text()').extract_first()
            # from_url = response.xpath('/html/body/div/div/div[2]/div/div/a/@href').extract_first()
            # if from_url[0:4] != 'http':
            #     from_url = 'http://www.yoka.com' + response.xpath('/html/body/div/div/div[2]/div/div/a/@href').extract_first()
            from_url = response.urljoin(response.xpath('//div[@class="infoTime"]/div/a/@href').extract_first())
            item['come_from'] = from_text + ':' + from_url
            # 内容详情
            quote = response.xpath('//div[@class="double_quotes"]/div/text()').extract_first().strip()
            detail_text = response.xpath('//div[@class="textCon"]/p/text()').extract()
            deal_text = ' '.join([i.strip() for i in detail_text])
            item['content_detail'] = quote + deal_text
            # 详情页图片地址
            detail_img_url = response.xpath('//div[@class="textCon"]/div/a/img/@src').extract()
            item['detail_img_url'] = ';'.join([i.strip() for i in detail_img_url])
            # print("item['detail_img_url']", item['detail_img_url'])
            # print('item', item)
            yield item
        else:
            # 无编辑者（轮播布局）
            item['compiler'] = '--'
            # 来源于
            from_text = response.xpath('//div[contains(@class, "g-content")]/ul/li[1]/a/text()').extract_first()
            if not from_text:
                from_text = response.xpath('//li[contains(text(),"来源于：")]/a/text()').extract_first()
            from_url = response.urljoin(response.xpath('/html/body/div/div/ul/li[1]/a/@href').extract_first())
            item['come_from'] = from_text + ':' + from_url
            # 内容详情
            detail_text = response.xpath('//dl[@class="text"]/dd//text()').extract_first().strip()
            # print('==========', detail_text, response.url)
            if not detail_text:
                detail_text = '--------------------'
            item['content_detail'] = detail_text
            # print("item['content_detail']", item['link_url'], item['content_detail'])
            # 详情页图片地址
            detail_img_url = response.xpath('//*[@id="list"]/ul/li/a/img/@src').extract()
            item['detail_img_url'] = ';'.join([i.strip() for i in detail_img_url])
            # print("item['detail_img_url']", item['detail_img_url'])
            next_url_list = response.xpath('//*[@id="list"]/ul/li/a/@href').extract()
            if next_url_list:
                for i in range(1, len(next_url_list)):
                    yield scrapy.Request(
                        method="GET",
                        url=next_url_list[i],
                        callback=self.parse_next_url,
                        meta={'item': deepcopy(item)}
                    )
                    pass

    def parse_next_url(self, response):
        """获取下一页数据"""
        item = response.meta['item']
        old_content_detail = item['content_detail']
        new_content_detail = response.xpath('//dl[@class="text"]/dd//text()').extract_first().strip()
        item['content_detail'] = old_content_detail + ';' + new_content_detail
        # print('item', item)
        yield item

    def get_release_time(self, item):
        try:
            # 发布时间格式处理
            split_list = item['link_url'].split('/')
            if split_list:
                release_time = split_list[5] + '-' + split_list[6][:2] + '-' + split_list[6][2:]
                item['release_time'] = release_time if release_time else self.nowData
            else:
                item['release_time'] = self.nowData
        except Exception as e:
            print(e)
