# -*- coding: utf-8 -*-
import datetime
from copy import deepcopy

import scrapy

from yoka_spider.items import YokaSpiderItem
from yoka_spider.log import logger


class YokabeautycolumnSpider(scrapy.Spider):
    name = 'yokaBeautyColumn'
    allowed_domains = ['yoka.com']
    # start_urls = ['http://yoka.com/']

    def start_requests(self):
        try:
            self.nowData = str(datetime.datetime.now())[0:10]
            self.getDataDate = ['2019', '2018', '2017']
            self.headers = {"Host": " www.yoka.com",
                            "User-Agent: Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv": "68.0) Gecko/20100101 Firefox/68.0",
                            "Accept": " text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
                            "Accept-Language": " zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2",
                            "Accept-Encoding": " gzip, deflate",
                            "Connection": " keep-alive"}
            item = YokaSpiderItem()
            # item = {}
            item['site_name'] = '优卡网'
            item['domain'] = 'www.yoka.com'
            item['domain_url'] = 'http://www.yoka.com/'
            item['first_title'] = '优卡网-时尚'
            item['first_title_url'] = 'http://beauty.yoka.com/'
            yield scrapy.Request(
                method="GET",
                url=item['first_title_url'],
                headers=self.headers,
                callback=self.parse_info,
                meta={'item': item}
            )
            print('时尚栏目板块数据抓取-----------------------------------')
        except Exception as e:
            print("start_requests:{}".format(e))
            logger.info("start_requests:{}".format(e))

    def parse_info(self, response):
        """获取内页信息"""
        item = response.meta['item']
        # todo:获取有焦点栏详情标题等-'//*[@id="fFocus"]/div/div[contains(@class,"item")]'
        details_focus = response.xpath('//*[@id="fFocus"]/div/div[contains(@class,"item")]')
        if details_focus:
            for index, detail in enumerate(details_focus):
                # 栏目模块名称
                item['second_title'] = '首页-时尚-焦点栏'
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
        # todo:获取有焦点栏下-左 数据-'//div[@class="gListBox"]/div'
        details_focus_dl = response.xpath('//div[@class="gListBox"]/div')
        for detail in details_focus_dl:
            # 栏目模块名称
            item['second_title'] = '首页-时尚-焦点栏下-左'
            item['second_title_url'] = item['first_title_url']
            # 栏目等级
            item['column_level'] = '二级栏目'
            # 详情标题
            item['title_detail'] = detail.xpath('./div/a/text()').extract_first()
            # 详情链接
            item['link_url'] = response.urljoin(detail.xpath('./div/a/@href').extract_first())
            # print("item['link_url']", item['link_url'])
            # 图片url
            item['img_url'] = detail.xpath('./div/a/img/@src').extract_first()
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
            if not item.get('img_url'):
                item['title_detail'] = response.xpath('//div[@class="textCon"]/div/a/img/@src').extract_first()
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
                if not item['title_detail']:
                    item['title_detail'] = response.xpath('//*[@id="picTitle"]/text()').extract_first()
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
            with open('error_club_item.txt', 'a') as f:
                f.write((str(item)) + '\n')
            print("get_release_time:{}".format(e))
            logger.info("get_release_time:{}".format(e))
        return []
