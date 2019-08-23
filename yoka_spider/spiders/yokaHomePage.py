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


class YokaHomePageSpider(scrapy.Spider):
    name = 'yokaHomePage'
    allowed_domains = ['yoka.com']

    def start_requests(self):
        try:
            # 第一版板块
            # 进行起始 url 的拼接
            url_list = {'http://www.yoka.com/': '首页'}
            # first_title = ['时尚', '美容', '奢华', '明星', '乐活', '男士', '视频', '独家', '社区', '品牌']
            self.nowData = str(datetime.datetime.now())[0:10]
            self.getDataDate = ['2019', '2018', '2017']
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
            item['first_title'] = '优卡网-首页'
            item['first_title_url'] = 'http://www.yoka.com/'
            yield scrapy.Request(
                method="GET",
                url=item['first_title_url'],
                headers=self.headers,
                callback=self.parse_info,
                meta={'item': item}
            )
            print('首页栏目数据抓取完成-----------------------------------')
        except Exception as e:
            print("start_requests:{}".format(e))
            logger.info("start_requests:{}".format(e))

    def parse_info(self, response):
        """获取内页信息"""
        item = response.meta['item']
        # todo:获取有焦点栏详情标题等
        details_focus = response.xpath('//*[@id="fFocus"]/div/div[contains(@class,"item")]')
        if details_focus:
            for index, detail in enumerate(details_focus):
                # 栏目模块名称
                item['second_title'] = '首页-焦点栏'
                item['second_title_url'] = item['first_title_url']
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
                    if res[0:4] in self.getDataDate:
                        yield scrapy.Request(
                            method="GET",
                            url=item['link_url'],
                            callback=self.parse_detail,
                            meta={'item': deepcopy(item)}
                        )
        # todo 获取焦点栏下-左信息
        # 获取焦点栏下-左信息
        focus_down_dl = response.xpath('//div[@class="g-content"]/div/div[@class="gLeft"]/div')
        if focus_down_dl:
            for detail in focus_down_dl:
                # 栏目模块名称
                item['second_title'] = '首页-焦点栏下左'
                item['second_title_url'] = item['first_title_url']
                # 栏目等级
                item['column_level'] = '二级栏目'
                # 详情链接标题
                item['title_detail'] = detail.xpath('./div[@class="g-imgText"]/a/em/text()').extract_first()
                if not item['title_detail']:
                    item['title_detail'] = detail.xpath('./div[@class="g-list"]/div[@class="tit"]/a/text()').extract_first()
                # 详情链接
                item['link_url'] = response.urljoin(detail.xpath('./div[@class="g-imgText"]/a/@href').extract_first())
                if not item['link_url']:
                    item['link_url'] = response.urljoin(detail.xpath('./div[@class="g-list"]/div[@class="tit"]/a/@href').extract_first())
                # 图片url
                item['img_url'] = detail.xpath('./div[@class="g-imgText"]/a/img/@src').extract_first()
                if not item['img_url']:
                    item['img_url'] = detail.xpath('./div[@class="g-list"]/div[@class="img"]/a/img/@src').extract_first()
                if item['link_url']:
                    # 发布时间
                    res = self.get_release_time(item)
                    if res:
                        if res[0:4] in self.getDataDate:
                            yield scrapy.Request(
                                method="GET",
                                url=item['link_url'],
                                callback=self.parse_detail,
                                meta={'item': deepcopy(item)}
                            )

        # todo 获取焦点栏下-右信息
        # 获取焦点栏下-右-上信息
        focus_down_rt_url = response.xpath('//div[@class="ad_first"]/div/script/@src').extract_first()
        if focus_down_rt_url:
            # 栏目模块名称
            item['second_title'] = '首页-焦点栏下-右上'
            item['second_title_url'] = item['first_title_url']
            # 栏目等级
            item['column_level'] = '二级栏目'
            yield scrapy.Request(
                method="GET",
                url=focus_down_rt_url,
                callback=self.parse_no_img_data,
                meta={'item': deepcopy(item)}
            )
        else:
            focus_down_rt_url = response.xpath('//div[@class="ad_first"]/div/div/a/@href').extract_first()
            # 栏目模块名称
            item['second_title'] = '首页-焦点栏下-右-上'
            item['second_title_url'] = item['first_title_url']
            # 栏目等级
            item['column_level'] = '二级栏目'
            # # 详情链接标题
            # item['title_detail'] = response.xpath('//div[@class="top_r"]/div/a/em/text()').extract_first()
            # 详情链接
            item['link_url'] = response.urljoin(focus_down_rt_url)
            # 图片url
            item['img_url'] = response.xpath('//div[@class="ad_first"]/div/div/a/img/@src').extract_first()
            if item['link_url']:
                # 发布时间
                res = self.get_release_time(item)
                if res:
                    if res[0:4] in self.getDataDate:
                        yield scrapy.Request(
                            method="GET",
                            url=item['link_url'],
                            callback=self.parse_detail,
                            meta={'item': deepcopy(item)}
                        )
        # 获取焦点栏下-右-中信息
        focus_down_rm = response.xpath('//div[@class="ad_first"]/ul/li')
        for detail in focus_down_rm:
            # 栏目模块名称
            item['second_title'] = '首页-焦点栏下-右中'
            item['second_title_url'] = item['first_title_url']
            # 栏目等级
            item['column_level'] = '二级栏目'
            focus_down_rm_url = detail.xpath('./script/@src').extract_first()
            yield scrapy.Request(
                method="GET",
                url=focus_down_rm_url,
                callback=self.parse_no_img_data,
                meta={'item': deepcopy(item)}
            )
        # 获取焦点栏下-右-下信息
        focus_down_rd = response.xpath('//*[@id="today_news"]/div')
        if focus_down_rd:
            for detail in focus_down_rd:
                # 栏目模块名称
                item['second_title'] = '首页-焦点栏下右'
                item['second_title_url'] = item['first_title_url']
                # 栏目等级
                item['column_level'] = '二级栏目'
                # 详情链接标题
                item['title_detail'] = detail.xpath('./div/a/text()').extract_first()
                # 详情链接
                item['link_url'] = response.urljoin(detail.xpath('./div/a/@href').extract_first())
                # 图片url
                item['img_url'] = '--'
                if item['link_url']:
                    # 发布时间
                    res = self.get_release_time(item)
                    if res:
                        if res[0:4] in self.getDataDate:
                            yield scrapy.Request(
                                method="GET",
                                url=item['link_url'],
                                callback=self.parse_detail,
                                meta={'item': deepcopy(item)}
                            )

        # todo:获取带有广告栏目数据
        # 广告栏-左信息
        ad_l_url = response.xpath('//*[@id="firstFs"]/div/div/script/@src')
        if ad_l_url:
            for ad_url in ad_l_url:
                # 栏目模块名称
                item['second_title'] = '首页-独家策划上-广告栏-左'
                item['second_title_url'] = item['first_title_url']
                # 栏目等级
                item['column_level'] = '二级栏目'
                ad_url = response.xpath('//*[@id="firstFs"]/div/div/script/@src').extract_first()
                yield scrapy.Request(
                    method="GET",
                    url=ad_url,
                    callback=self.parse_no_img_data,
                    meta={'item': deepcopy(item)}
                )
        else:
            ad_l = response.xpath('//*[@id="firstFs"]/div/div/div/a/@href').extract_first()
            if ad_l:
                # for detail in ad_r:
                    # 栏目模块名称
                    item['second_title'] = '首页-广告栏-左'
                    item['second_title_url'] = item['first_title_url']
                    # 栏目等级
                    item['column_level'] = '二级栏目'
                    # # 详情链接标题
                    # item['title_detail'] = detail.xpath('./div/a/text()').extract_first()
                    # 详情链接
                    item['link_url'] = response.urljoin(response.xpath('//*[@id="firstFs"]/div/div/div/a/@href').extract_first())
                    # 图片url
                    item['img_url'] = response.urljoin(response.xpath('//*[@id="firstFs"]/div/div/div/a/img/@src').extract_first())
                    # print(item['img_url'])
                    if item['link_url']:
                        # 发布时间
                        res = self.get_release_time(item)
                        if res:
                            if res[0:4] in self.getDataDate:
                                yield scrapy.Request(
                                    method="GET",
                                    url=item['link_url'],
                                    callback=self.parse_detail,
                                    meta={'item': deepcopy(item)}
                                )
        # 广告栏-右信息
        ad_r_url = response.xpath('//*[@id="firstFsR"]/div/div/script/@src').extract_first()
        if ad_r_url:
            # 栏目模块名称
            item['second_title'] = '首页-广告栏-右'
            item['second_title_url'] = item['first_title_url']
            # 栏目等级
            item['column_level'] = '二级栏目'
            ad_url = response.urljoin(ad_r_url)
            yield scrapy.Request(
                method="GET",
                url=ad_url,
                callback=self.parse_no_img_data,
                meta={'item': deepcopy(item)}
            )

        # todo:独家策划栏目信息
        # 独家策划栏目-左
        exclusive_plans_l = response.xpath('//*[@id="feature_box"]/div')
        if exclusive_plans_l:
            for detail in exclusive_plans_l:
                # 栏目模块名称
                item['second_title'] = '首页-独家策划-左'
                item['second_title_url'] = item['first_title_url']
                # 栏目等级
                item['column_level'] = '二级栏目'
                # 详情链接标题
                item['title_detail'] = '首页-独家策划-左'
                # 详情链接
                item['link_url'] = response.urljoin(detail.xpath('./a/@href').extract_first())
                # 图片url
                item['img_url'] = response.urljoin(detail.xpath('./a/img/@src').extract_first())
                # print(item['img_url'])
                # 发布时间
                item['release_time'] = '--'
                # 编辑者
                item['compiler'] = '--'
                # 来源于
                item['come_from'] = '--'
                # 内容详情
                item['content_detail'] = '--'
                # 详情页图片地址
                item['detail_img_url'] = '--'
                yield item
        # 独家策划栏目-右
        exclusive_plans_r = response.xpath('//div[@class="tag_try"]/div/span/text()').extract()
        if exclusive_plans_r:
            for second_title in exclusive_plans_r:
                # 栏目模块名称
                # second_title = planR.xpath('./span/text()').extract_first()
                item['second_title_url'] = item['first_title_url']
                # 栏目等级
                item['column_level'] = '二级栏目'
                if second_title == '热门试用':
                    item['second_title'] = '首页-独家策划-右-' + second_title
                    for detail in response.xpath('//*[@id="try_scroll"]/div/div/a'):
                        # 详情链接标题
                        item['title_detail'] = detail.xpath('./div[@class="title fcut"]/text()').extract_first()
                        # 详情链接
                        item['link_url'] = response.urljoin(detail.xpath('./@href').extract_first())
                        # 图片url
                        item['img_url'] = response.urljoin(detail.xpath('./div/img/@src').extract_first())
                        # print(item['img_url'])
                        # 发布时间
                        item['release_time'] = '--'
                        # 编辑者
                        item['compiler'] = '--'
                        # 来源于
                        item['come_from'] = '--'
                        # 内容详情
                        item['content_detail'] = '--'
                        # 详情页图片地址
                        item['detail_img_url'] = '--'
                        yield item
                elif second_title == '新品评测':
                    item['second_title'] = '首页-独家策划-右-' + second_title
                    for detail in response.xpath('//*[@id="pingce_scroll"]/div/div/a'):
                        # 详情链接标题
                        item['title_detail'] = detail.xpath('./div[contains(@class,"title")]/text()').extract_first()
                        # 详情链接
                        item['link_url'] = response.urljoin(detail.xpath('./@href').extract_first())
                        # 图片url
                        item['img_url'] = response.urljoin(detail.xpath('./div/img/@src').extract_first())
                        # print(item['img_url'])
                        if item['link_url']:
                            # 发布时间
                            res = self.get_release_time(item)
                            if res:
                                if res[0:4] in self.getDataDate:
                                    yield scrapy.Request(
                                        method="GET",
                                        url=item['link_url'],
                                        callback=self.parse_detail,
                                        meta={'item': deepcopy(item)}
                                    )

        # todo:时装FASHION/美容BEAUTY/明星STAR/奢华LUXURY/乐活LIFESTYLE/先锋红人栏目信息
        column_titles = response.xpath('//div[contains(@class, "g-title")]/div/strong/a/text()').extract()
        column_foucs_lt = response.xpath('//div[@class="g-content"]/div[@class="gLeft"]/div/div[@class="foucs"]/div/a')
        if column_foucs_lt:
            for foucs in column_foucs_lt:
                # 左上-焦点栏目数据
                # 栏目模块名称
                item['second_title'] = '首页-' + column_titles[column_foucs_lt.index(foucs)] + '-焦点栏'
                item['second_title_url'] = item['first_title_url']
                # 栏目等级
                item['column_level'] = '三级栏目'
                # 详情链接标题
                item['title_detail'] = foucs.xpath('./div/text()').extract_first()
                # 详情链接
                item['link_url'] = foucs.xpath('./@href').extract_first()
                # 图片url
                item['img_url'] = foucs.xpath('./img/@src').extract_first()
                # print(item['img_url'])
                # 发布时间
                item['release_time'] = '--'
                # 编辑者
                item['compiler'] = '--'
                # 来源于
                item['come_from'] = '--'
                # 内容详情
                item['content_detail'] = '--'
                # 详情页图片地址
                item['detail_img_url'] = '--'
                yield item
                # 时装FASHION/美容BEAUTY/明星STAR/奢华LUXURY/乐活LIFESTYLE/先锋达人 - 左下
                column_foucs_ld = response.xpath('//div[@class="gLeft"]/div[contains(@class,"fashList")]')
                if column_foucs_ld:
                    for aNode in column_foucs_ld:
                        # 栏目模块名称
                        item['second_title'] = '首页-' + column_titles[column_foucs_ld.index(aNode)] + '-焦点栏下'
                        item['second_title_url'] = item['first_title_url']
                        # 栏目等级
                        item['column_level'] = '三级栏目'
                        # 详情链接标题
                        item['title_detail'] = aNode.xpath('./div/div[2]/a/text()').extract_first()
                        # 详情链接
                        item['link_url'] = response.urljoin(aNode.xpath('./div/div[1]/a/@href').extract_first())
                        # 图片url
                        item['img_url'] = response.xpath('./div/div[1]/a/img/@src').extract_first()
                        if item['link_url']:
                            # 发布时间
                            res = self.get_release_time(item)
                            if res:
                                if res[0:4] in self.getDataDate:
                                    yield scrapy.Request(
                                        method="GET",
                                        url=item['link_url'],
                                        callback=self.parse_detail,
                                        meta={'item': deepcopy(item)}
                                    )
            # 时装FASHION/美容BEAUTY/明星STAR/奢华LUXURY/乐活LIFESTYLE/先锋达人 - 右上
            fash_she_Lt = response.xpath('//div[@class="gRight"]/div[@class="g-pImg margB"]')
            happy_lt = response.xpath('//div[@class="gRight"]/div[@class="TopicIn"]')
            xf_lt = response.xpath('//div[@class="gRight"]/div[@class="darenRc"]')
            fash_she_Lt.extend(happy_lt)
            fash_she_Lt.extend(xf_lt)
            if fash_she_Lt:
                for detail in fash_she_Lt:
                    # 栏目模块名称
                    item['second_title'] = '首页-时装/奢华/美容-右'
                    item['second_title_url'] = item['first_title_url']
                    # 栏目等级
                    item['column_level'] = '三级栏目'
                    # 详情链接标题
                    item['title_detail'] = detail.xpath('.//a/dl/dt/text()').extract_first()
                    # 详情链接
                    link_url = response.urljoin(detail.xpath('./a/@href').extract_first())
                    if not link_url:
                        link_url = response.urljoin(detail.xpath('./div/a/@href').extract_first())
                    item['link_url'] = link_url
                    # 图片url
                    img_url = detail.xpath('./a/img/@src').extract_first()
                    if not img_url:
                        img_url = detail.xpath('./div/a/img/@src').extract_first()
                        if not img_url:
                            img_url = detail.xpath('./div/img/@src').extract_first()
                        else:
                            img_url = '--'
                    item['img_url'] = img_url
                    if item['link_url']:
                        # 发布时间
                        res = self.get_release_time(item)
                        if res:
                            if res[0:4] in self.getDataDate:
                                yield scrapy.Request(
                                    method="GET",
                                    url=item['link_url'],
                                    callback=self.parse_detail,
                                    meta={'item': deepcopy(item)}
                                )
            # 时装FASHION/美容BEAUTY/明星STAR/奢华LUXURY/乐活LIFESTYLE/先锋达人 - 右中焦点栏
            fash_she_Lj = response.xpath('//div[@class="g-content"]/div[@class="gRight"]/div/div[@class="foucs"]/div')
            for detail in fash_she_Lj:
                # 栏目模块名称
                item['second_title'] = '首页-时装/明星-右中焦点'
                item['second_title_url'] = item['first_title_url']
                # 栏目等级
                item['column_level'] = '三级栏目'
                # 详情链接标题
                item['title_detail'] = detail.xpath('./a/dl/dt/text()').extract_first()
                # 详情链接
                item['link_url'] = response.urljoin(detail.xpath('./a/@href').extract_first())
                # 图片url
                item['img_url'] = response.urljoin(detail.xpath('./a/img/@src').extract_first())
                if item['link_url']:
                    # 发布时间
                    res = self.get_release_time(item)
                    if res:
                        if res[0:4] in self.getDataDate:
                            yield scrapy.Request(
                                method="GET",
                                url=item['link_url'],
                                callback=self.parse_detail,
                                meta={'item': deepcopy(item)}
                            )

            # 时装FASHION/美容BEAUTY/明星STAR/奢华LUXURY/乐活LIFESTYLE/先锋达人 - 右下-top榜单/达人心得
            fashion_rx = response.xpath('//div[@class="g-content"]/div[@class="gRight"]/div')
            for detail in fashion_rx:
                # 栏目模块名称
                item['second_title'] = '首页-时装/美容/明星/奢华/乐活-右下'
                second_title = detail.xpath('./div[contains(@class, "tit")]//text()').extract_first()
                print('second_title', second_title)
                if second_title == '达人心得':
                    item['second_title'] = '首页-美容BEAUTY-' + second_title
                    for aNode in detail.xpath('./div/dl'):
                        item['title_detail'] = aNode.xpath('./dd/strong/a/text()').extract_first()
                        # 详情链接
                        item['link_url'] = response.urljoin(aNode.xpath('./dd/strong/a/@href').extract_first())
                        # 图片url
                        item['img_url'] = response.urljoin(aNode.xpath('./dt/a/img/@src').extract_first())
                        yield scrapy.Request(
                            method="GET",
                            url=item['link_url'],
                            callback=self.yeil_no_detail_func,
                            meta={'item': deepcopy(item)}
                        )
                elif detail.xpath('./div[contains(@class, "tit")]/span/text()').extract_first() == 'top榜单':
                    item['second_title'] = '首页-明星STAR-' + detail.xpath('./div[contains(@class, "tit")]/span/text()').extract_first()
                    for aNode in detail.xpath('./div/div[@class="list"]'):
                        item['title_detail'] = aNode.xpath('./a/text()').extract_first()
                        # 详情链接
                        item['link_url'] = response.urljoin(aNode.xpath('./a/@href').extract_first())
                        # 图片url
                        item['img_url'] = '--'
                        # 发布时间
                        res = self.get_release_time(item)
                        if res:
                            if res[0:4] in self.getDataDate:
                                yield scrapy.Request(
                                    method="GET",
                                    url=item['link_url'],
                                    callback=self.parse_detail,
                                    meta={'item': deepcopy(item)}
                                )
                else:
                    item['second_title_url'] = item['first_title_url']
                    # 栏目等级
                    item['column_level'] = '三级栏目'
                    # # 详情链接标题
                    item['title_detail'] = detail.xpath('./div/a/text()').extract_first()
                    if not item['title_detail']:
                        item['title_detail'] = detail.xpath('./div[@class="txt"]/text()').extract_first()
                    # 详情链接
                    item['link_url'] = response.urljoin(detail.xpath('./div[@class="tit"]/a/@href').extract_first())
                    if not item['link_url']:
                        item['link_url'] = response.urljoin(detail.xpath('./a/@href').extract_first())
                    # 图片url
                    item['img_url'] = response.urljoin(detail.xpath('/div[@class="img"]/a/img/@src').extract_first())
                    # print(item['img_url'])
                    if item['link_url']:
                        # 发布时间
                        res = self.get_release_time(item)
                        if res:
                            if res[0:4] in self.getDataDate:
                                yield scrapy.Request(
                                    method="GET",
                                    url=item['link_url'],
                                    callback=self.parse_detail,
                                    meta={'item': deepcopy(item)}
                                )

        # todo:乐活上栏目信息
        life_style_up = response.xpath('//div[@class="g-ads-three clearfix"]/div/div')
        for detail in life_style_up:
            # 栏目模块名称
            item['second_title'] = '首页-乐活LIFESTYLE-上'
            item['second_title_url'] = item['first_title_url']
            # 栏目等级
            item['column_level'] = '三级栏目'
            # 详情链接标题
            item['title_detail'] = detail.xpath('./div/a/text()').extract_first()
            # 详情链接dgf
            item['link_url'] = response.urljoin(detail.xpath('./div/a/@href').extract_first())
            # 图片url
            item['img_url'] = response.urljoin(detail.xpath('./div/a/img/@src').extract_first())
            if item['link_url']:
                # 发布时间
                res = self.get_release_time(item)
                if res:
                    if res[0:4] in self.getDataDate:
                        yield scrapy.Request(
                            method="GET",
                            url=item['link_url'],
                            callback=self.parse_detail,
                            meta={'item': deepcopy(item)}
                        )

    def yeil_no_detail_func(self, response):
        item = response.meta['item']
        # 发布时间
        item['release_time'] = response.xpath('//div[@class="title_xinde"]/dl/dd/em/text()').extract_first()
        # 编辑者
        item['compiler'] = response.xpath('//*[@id="hzp-login"]/div/dl/dd[1]/h2/a/text()').extract_first()
        if not item['compiler']:
            item['compiler'] = '--'
        # 来源于
        item['come_from'] = response.xpath('//div[@class="hzp-nav"]/div/dl/dt/a/@href').extract_first()
        if not item['come_from']:
            item['come_from'] = '--'
        # 内容详情
        content_detail = response.xpath('//div[contains(@class, "xinde_contentBox")]/p/text()').extract()
        if not content_detail:
            content_detail = response.xpath('//div[contains(@class, "xinde_contentBox")]/p/span/text()').extract()
        else:
            content_detail = ['--']
        item['content_detail'] = ' '.join([i.strip() for i in content_detail])
        # 详情页图片地址
        detail_img_url = response.xpath('//div[contains(@class, "xinde_contentBox")]/p/img/@src').extract()
        if not detail_img_url:
            detail_img_url = response.xpath('//div[contains(@class, "xinde_contentBox")]/div/a/img/@src').extract()
        else:
            detail_img_url = ['--']
        item['detail_img_url'] = ';'.join([i.strip() for i in detail_img_url])
        yield item

    def parse_no_img_data(self, response):
        item = response.meta['item']
        # print(response.text)
        # 详情链接标题
        item['title_detail'] = response.xpath('//div/a/text()').extract_first()
        if not item['title_detail']:
            item['title_detail'] = response.xpath('//a/text()').extract_first()
        # 详情链接
        item['link_url'] = response.urljoin(response.xpath('//a/@href').extract_first())
        if not item['link_url']:
            item['link_url'] = response.urljoin(response.xpath('//a/@href').extract_first())
        # 图片url
        item['img_url'] = response.urljoin(response.xpath('//div/a/img/@href').extract_first())
        if not item['img_url']:
            item['img_url'] = response.urljoin(response.xpath('//a/img/@href').extract_first())
        if item['link_url']:
            # 发布时间
            res = self.get_release_time(item)
            if res:
                if res[0:4] in self.getDataDate:
                    yield scrapy.Request(
                        method="GET",
                        url=item['link_url'],
                        callback=self.parse_detail,
                        meta={'item': deepcopy(item)}
                    )

    def parse_detail(self, response):
        """获取详情内容和发布时间"""
        # item = YokaSpiderItem()
        item = response.meta['item']
        auther = response.xpath('/html/body/div/div/div[2]/div/dl/dd/i/text()').extract_first()
        if not auther:
            auther = response.xpath('//div[@class="infoTime"]/dl/dd/i/text()').extract_first()
        if auther:
            # # 详情链接标题
            if not item.get('title_detail'):
                item['title_detail'] = response.xpath('//div[contains(@class, "g-content")]//div/h1/text()').extract_first()
                if not item['title_detail']:
                    item['title_detail'] = response.xpath('//div[contains(@class, "g-content")]//div/h1/text()').extract_first()
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
                release_time = split_list[-3] + '-' + split_list[-2][0:2] + '-' + split_list[-2][2:4]
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