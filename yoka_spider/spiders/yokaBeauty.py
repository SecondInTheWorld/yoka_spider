# -*- coding: utf-8 -*-
import datetime
import json
import logging
import math
import re
from copy import deepcopy

import scrapy

from yoka_spider.items import YokaSpiderItem
from yoka_spider.log import logger


class YokaBeautySpider(scrapy.Spider):
    name = 'yokaBeauty'
    allowed_domains = ['yoka.com']

    def start_requests(self):
        try:
            # 第一版板块
            # 进行起始 url 的拼接
            url_list = {'http://fashion.yoka.com/': '时尚', 'http://beauty.yoka.com/': '美容',
                        'http://luxury.yoka.com/': '奢华',
                        'http://star.yoka.com/': '明星', 'http://life.yoka.com/': '乐活', 'http://www.yokamen.cn/': '男士',
                        'http://www.yoka.com/video/': '视频', 'http://www.yoka.com/z/': '独家',
                        'http://bbs.yoka.com/': '社区',
                        'http://brand.yoka.com/': '品牌'}
            # first_title = ['时尚', '美容', '奢华', '明星', '乐活', '男士', '视频', '独家', '社区', '品牌']
            self.nowData = str(datetime.datetime.now())[0:10]
            self.getDataDate = ['2019-07']
            self.headers = {"Host": " www.yoka.com",
                            "User-Agent: Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv": "68.0) Gecko/20100101 Firefox/68.0",
                            "Accept": " text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
                            "Accept-Language": " zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2",
                            "Accept-Encoding": " gzip, deflate",
                            "Connection": " keep-alive"}
            # for key, value in url_list.items():
            # 一级栏目
            item = YokaSpiderItem()
            # item = {}
            item['site_name'] = '优卡网'
            item['domain'] = 'www.yoka.com'
            item['domain_url'] = 'http://www.yoka.com/'
            item['first_title'] = '优卡网-首页-' + url_list['http://beauty.yoka.com/']
            item['first_title_url'] = 'http://beauty.yoka.com/'
            yield scrapy.Request(
                method="GET",
                url=item['first_title_url'],
                headers=self.headers,
                callback=self.parse,
                meta={'item': item}
            )
            print('美容栏目url请求发送完成-----------------------------------')
        except Exception as e:
            print("YokaBeautySpider.start_requests:{}".format(e))
            logger.info("YokaBeautySpider.start_requests:{}".format(e))

    def parse(self, response):
        """获取第二层栏目信息"""
        item = response.meta['item']
        # 获取第二层栏目url
        for aNode in response.xpath('//*[@id="p_nav_box_high"]/a'):
            # 二级栏目
            item['second_title'] = item['first_title'] + '-' + aNode.xpath('./text()').extract_first()
            item['second_title_url'] = aNode.xpath('./@href').extract_first()
            # if item['second_title'] == '优卡网-首页-时尚-时尚圈':
            #     print('club data-------------')
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
                if item['link_url']:
                    # 发布时间
                    res = self.get_release_time(item)
                    if res[0:7] in self.getDataDate:
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
                # 栏目等级
                item['column_level'] = '--'
                # 详情
                item['title_detail'] = detail.xpath('./div[@class="tit"]/a/text()').extract_first()
                # 详情链接
                item['link_url'] = response.urljoin(detail.xpath('./div[@class="tit"]/a[1]/@href').extract_first())
                # print("item['link_url']---box", item['link_url'])
                # 图片url
                item['img_url'] = detail.xpath('./div[@class="img"]/a/img/@src').extract_first()
                if item['link_url']:
                    # 发布时间
                    res = self.get_release_time(item)
                    if res[0:7] in self.getDataDate:
                        yield scrapy.Request(
                            method="GET",
                            url=item['link_url'],
                            callback=self.parse_detail,
                            meta={'item': deepcopy(item)}
                        )

        # todo:获取评测类数据
        # 新品评测栏目数据
        details_new_pro = response.xpath('//div[@class="newEvalu"]/dl')
        if details_new_pro:
            for detail in details_new_pro:
                # 栏目等级
                item['column_level'] = '--'
                # 详情标题
                item['title_detail'] = detail.xpath('./dd/h3/a/text()').extract_first()
                # 详情链接
                item['link_url'] = response.urljoin(detail.xpath('./dt/a/@href').extract_first())
                # print("item['link_url']", item['link_url'])
                # 图片url
                item['img_url'] = response.urljoin(detail.xpath('./dt/a/img/@src').extract_first())
                if item['link_url']:
                    # 发布时间
                    res = self.get_release_time(item)
                    if res[0:7] in self.getDataDate:
                        yield scrapy.Request(
                            method="GET",
                            url=item['link_url'],
                            callback=self.parse_detail,
                            meta={'item': deepcopy(item)}
                        )
            # 评测优选
            details_val_opt = response.xpath('//div[contains(@class, "g-main")]/div')
            if details_val_opt:
                for detail in details_val_opt:
                    # 栏目等级
                    item['column_level'] = '--'
                    # 详情标题
                    item['title_detail'] = detail.xpath('./div/dl/dt/a/text()').extract_first()
                    # 详情链接
                    item['link_url'] = response.urljoin(detail.xpath('./div/dl/dt/a/@href').extract_first())
                    # print("item['link_url']", item['link_url'])
                    # 图片url
                    item['img_url'] = response.urljoin(detail.xpath('./div/div[@class="pic"]/a/img/@src').extract_first())
                    if item['link_url']:
                        # 发布时间
                        res = self.get_release_time(item)
                        if res[0:7] in self.getDataDate:
                            yield scrapy.Request(
                                method="GET",
                                url=item['link_url'],
                                callback=self.parse_detail,
                                meta={'item': deepcopy(item)}
                            )
            # 主题评测
            theme_divs = response.xpath('//*[@id="subCont"]/div')
            if theme_divs:
                for detail in theme_divs:
                    # 栏目等级
                    item['column_level'] = '--'
                    # 详情标题
                    item['title_detail'] = detail.xpath('./dl/dd/a/text()').extract_first()
                    # 详情链接
                    item['link_url'] = response.urljoin(detail.xpath('./dl/dd/a/@href').extract_first())
                    # print("item['link_url']", item['link_url'])
                    # 图片url
                    item['img_url'] = response.urljoin(detail.xpath('./dl/dt/a/img/@src').extract_first())
                    if item['link_url']:
                        # 发布时间
                        res = self.get_release_time(item)
                        if res[0:7] in self.getDataDate:
                            yield scrapy.Request(
                                method="GET",
                                url=item['link_url'],
                                callback=self.parse_detail,
                                meta={'item': deepcopy(item)}
                            )
            # 达人评测
            nber_divs = response.xpath('//*[@id="pc_talentCon"]/div')
            if nber_divs:
                for detail in nber_divs:
                    # 栏目等级
                    item['column_level'] = '--'
                    # 详情标题
                    item['title_detail'] = detail.xpath('./dl[@class="b_b"]/dt/a/text()').extract_first()
                    # 详情链接
                    item['link_url'] = response.urljoin(detail.xpath('./dl[@class="b_b"]/dt/a/@href').extract_first())
                    # print("item['link_url']", item['link_url'])
                    # 图片url
                    item['img_url'] = response.urljoin(detail.xpath('./div/div/a/img/@src').extract_first())
                    if item['link_url']:
                        # 编辑者
                        item['compiler'] = response.xpath('./div/dl[@class="user"]/dd/text()')
                        yield scrapy.Request(
                            method="GET",
                            url=item['link_url'],
                            callback=self.parse_nber_detail,
                            meta={'item': deepcopy(item)}
                        )
            # 特别企划
            special_plan_divs = response.xpath('///*[@id="spe_tab_con"]/div')
            if special_plan_divs:
                for detail in special_plan_divs:
                    # 栏目等级
                    item['column_level'] = '--'
                    # 详情标题
                    item['title_detail'] = detail.xpath('./ul/li/a/h3/text()').extract_first()
                    # 详情链接
                    item['link_url'] = response.urljoin(detail.xpath('./ul/li/a/@href').extract_first())
                    # print("item['link_url']", item['link_url'])
                    # 图片url
                    item['img_url'] = response.urljoin(detail.xpath('./ul/li/a/span/img/@src').extract_first())
                    if item['link_url']:
                        # 编辑者
                        item['compiler'] = '--'
                        yield scrapy.Request(
                            method="GET",
                            url=item['link_url'],
                            callback=self.parse_special_plan_detail,
                            meta={'item': deepcopy(item)}
                        )
            # 热门评测报告
            hot_divs = response.xpath('//div[contains(@class, "hotEvalu")]/ul/li')
            if hot_divs:
                for detail in hot_divs:
                    # 栏目等级
                    item['column_level'] = '--'
                    # 详情标题
                    item['title_detail'] = detail.xpath('./a/text()').extract_first()
                    # 详情链接
                    item['link_url'] = response.urljoin(detail.xpath('./a/@href').extract_first())
                    # print("item['link_url']", item['link_url'])
                    # 图片url
                    item['img_url'] = '--'
                    if item['link_url']:
                        yield scrapy.Request(
                            method="GET",
                            url=item['link_url'],
                            callback=self.parse_hot_detail,
                            meta={'item': deepcopy(item)}
                        )
            # 测评-焦点栏目数据
            hot_divs = response.xpath('//*[@id="pics-focus"]/div/div')
            if hot_divs:
                for detail in hot_divs:
                    # 栏目等级
                    item['column_level'] = '一级栏目'
                    # 详情标题
                    item['title_detail'] = ' '.join([i.strip() for i in detail.xpath('./a/dl//text()').extract()])
                    # 详情链接
                    item['link_url'] = response.urljoin(detail.xpath('./a/@href').extract_first())
                    # print("item['link_url']", item['link_url'])
                    # 图片url
                    item['img_url'] = response.urljoin(detail.xpath('./a/img/@src').extract_first())
                    if item['link_url']:
                        # 发布时间
                        res = self.get_release_time(item)
                        if res[0:7] in self.getDataDate:
                            yield scrapy.Request(
                                method="GET",
                                url=item['link_url'],
                                callback=self.parse_detail,
                                meta={'item': deepcopy(item)}
                            )

        # todo:获取试用类数据

    def parse_hot_detail(self, response):
        item = response.meta['item']
        # 编辑者
        item['compiler'] = response.xpath('//*[@id="author_baidu"]/text()').extract_first()
        # 发布时间
        item['release_time'] = response.xpath('//*[@id="pubtime_baidu"]/text()').extract_first()
        # 来源于
        from_text = response.xpath('//*[@id="source_baidu"]/a/text()').extract_first()
        from_url = response.xpath('//*[@id="source_baidu"]/a/@href').extract_first()
        item['come_from'] = from_text + ':' + from_url
        # 内容详情
        content_detail = response.xpath('//div[contains(@class, "xinde_contentBox")]/p/text()').extract()
        item['content_detail'] = ' '.join([i.strip() for i in content_detail])
        # 详情页图片地址 //*[@id="informationContent"]/div/div/div/div/a/img/@src
        detail_img_url = response.xpath('//*[@id="informationContent"]/div/div/div/div/a/img/@src').extract()
        item['detail_img_url'] = ';'.join([i.strip() for i in detail_img_url])
        if item['release_time'][0:7] == self.nowData[0:7]:
            yield item

    def parse_special_plan_detail(self, response):
        item = response.meta['item']
        # 发布时间
        item['release_time'] = self.nowData
        # 来源于
        from_text = item['compiler']
        from_url = item['link_url']
        item['come_from'] = from_text + ':' + from_url
        # 内容详情
        item['content_detail'] = '--'
        # 详情页图片地址
        item['detail_img_url'] = item['img_url']
        yield item

    # 达人评测类详情页
    def parse_nber_detail(self, response):
        item = response.meta['item']
        # 发布时间
        item['release_time'] = response.xpath('//div[@class="title_xinde"]/dl/dd/em/text()')
        # 来源于
        from_text = item['compiler']
        from_url = item['link_url']
        item['come_from'] = from_text + ':' + from_url
        # 内容详情
        detail_text = response.xpath('//div[contains(@class, "xinde_contentBox")]/p/text()').extract()
        if not detail_text:
            detail_text = response.xpath('//div[contains(@class, "xinde_contentBox")]/text()').extract()
        item['content_detail'] = ' '.join([i.strip() for i in detail_text])
        # 详情页图片地址
        detail_img_url = response.xpath('//div[contains(@class, "xinde_contentBox")]/p/img/@src').extract()
        if not detail_img_url:
            detail_img_url = response.xpath('//div[contains(@class, "xinde_contentBox")]/img/@src')
        item['detail_img_url'] = ';'.join([i.strip() for i in detail_img_url])
        if item['release_time'][0:7] == self.nowData[0:7]:
            yield item

    def parse_detail(self, response):
        """获取详情内容和发布时间"""
        # item = YokaSpiderItem()
        item = response.meta['item']
        auther = response.xpath('/html/body/div/div/div[2]/div/dl/dd/i/text()').extract_first()
        if auther:
            # # 详情链接标题
            if not item.get('title_detail'):
                item['title_detail'] = response.xpath('//div[contains(@class, "g-content")]/div/h1/text()').extract_first()
            # 编辑者
            item['compiler'] = auther
            # 来源于
            from_text = response.xpath('//div[@class="infoTime"]/div/a/text()').extract_first()
            if not from_text:
                from_text = response.xpath('//li[contains(text(),"来源于：")]/a/text()').extract_first()
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
            # print('item', item)
            yield item
        else:
            if not item.get('title_detail'):
                item['title_detail'] = response.xpath('//div[contains(@class, "g-content")]/div/h1/text()').extract_first()
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
                release_time = split_list[5] + '-' + split_list[6][0:2] + '-' + split_list[6][2:4]
                item['release_time'] = release_time
                return release_time[0:7]
        except Exception as e:
            print("item", item)
            item['release_time'] = self.nowData
            with open('error_beauty_detail_url.txt', 'a') as f:
                f.write((str(item)) + '\n')
            print("get_release_time:{}".format(e))
            logger.info("get_release_time:{}".format(e))
        return []


def get_time():
    try:
        # 发布时间格式处理
        print(111)
        a=2
        b = a / 0
    except Exception as e:
        logger.info("get_release_time:{}".format(e))
        print("get_release_time:{}".format(e))
    finally:
        print('222222222')


if __name__ == '__main__':
    get_time()