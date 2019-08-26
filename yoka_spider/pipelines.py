# -*- coding: utf-8 -*-
import json

import json
import time
import pandas as pd
import copy
import pymysql

mysqlConfig = {'host': '59.111.106.192', 'port': 3306,
               'user': '|_|^spider^|_|', 'passwd': 'a19956171223',
               'db': 'YokaDB', 'charset': 'utf8mb4'}


class YokaDetailPipeline(object):
    """将详情数据插入到mysql数据库中"""

    def __init__(self):
        # 1. 建立数据库的连接
        # self.connect = pymysql.connect(
        #     host='59.111.106.192',
        #     port=3306,
        #     user='|_|^spider^|_|',
        #     passwd='a19956171223',
        #     db='YokaDB',
        #     charset='utf8mb4'
        # )
        self.connect = pymysql.connect(
            host='localhost',
            port=3306,
            user='root',
            passwd='mysql',
            db='yokaDB',
            charset='utf8mb4'
        )
        # 2. 创建一个游标cursor, 是用来操作表。
        self.cursor = self.connect.cursor()

    def process_item(self, item, spider):
        try:
            if spider.name == 'yokaClub':
                # 3. 将Item数据放入数据库，默认是同步写入。
                # insert_sql = "insert ignore into job(zwmc, zwxz, zpyq, gwyq) VALUES ('%s', '%s', '%s', '%s')" % (
                # item['zwmc'], item['zwxz'], item['zpyq'], item['gwyq'])
                insert_sql = """insert ignore into yoka_club_detail(site_name, domain, domain_url, 
                                first_title, first_title_url, second_title, second_title_url, column_level, 
                                price, title_detail, link_url, img_url, compiler, come_from, release_time, 
                                content_detail, detail_img_url) VALUES ('{site_name}', '{domain}', '{domain_url}', 
                                '{first_title}', '{first_title_url}', '{second_title}', '{second_title_url}', 
                                '{column_level}', '{price}', '{title_detail}', '{link_url}', '{img_url}', '{compiler}', 
                                '{come_from}', '{release_time}', '{content_detail}', '{detail_img_url}')""".format(
                    site_name=item['site_name'], domain=item['domain'], domain_url=item['domain_url'],
                    first_title=item['first_title'], first_title_url=item['first_title_url'],
                    second_title=item['second_title'],
                    second_title_url=item['second_title_url'], column_level=item['column_level'], price=2400,
                    title_detail=item['title_detail'], link_url=item['link_url'], img_url=item['img_url'],
                    compiler=item['compiler'], come_from=item['come_from'], release_time=item['release_time'],
                    content_detail=item['content_detail'], detail_img_url=item['detail_img_url'])

            elif spider.name == 'yokaBeauty':
                insert_sql = """insert ignore into yoka_beauty_detail(site_name, domain, domain_url, 
                                first_title, first_title_url, second_title, second_title_url, column_level, 
                                price, title_detail, link_url, img_url, compiler, come_from, release_time, 
                                content_detail, detail_img_url) VALUES ('{site_name}', '{domain}', '{domain_url}', 
                                '{first_title}', '{first_title_url}', '{second_title}', '{second_title_url}', 
                                '{column_level}', '{price}', '{title_detail}', '{link_url}', '{img_url}', '{compiler}', 
                                '{come_from}', '{release_time}', '{content_detail}', '{detail_img_url}')""".format(
                    site_name=item['site_name'], domain=item['domain'], domain_url=item['domain_url'],
                    first_title=item['first_title'], first_title_url=item['first_title_url'],
                    second_title=item['second_title'],
                    second_title_url=item['second_title_url'], column_level=item['column_level'], price=2400,
                    title_detail=item['title_detail'], link_url=item['link_url'], img_url=item['img_url'],
                    compiler=item['compiler'], come_from=item['come_from'], release_time=item['release_time'],
                    content_detail=item['content_detail'], detail_img_url=item['detail_img_url'])

            elif spider.name == 'yokaHomePage':
                insert_sql = """insert ignore into yoka_home_detail(site_name, domain, domain_url, 
                                first_title, first_title_url, second_title, second_title_url, column_level, 
                                price, title_detail, link_url, img_url, compiler, come_from, release_time, 
                                content_detail, detail_img_url) VALUES ('{site_name}', '{domain}', '{domain_url}', 
                                '{first_title}', '{first_title_url}', '{second_title}', '{second_title_url}', 
                                '{column_level}', '{price}', '{title_detail}', '{link_url}', '{img_url}', '{compiler}', 
                                '{come_from}', '{release_time}', '{content_detail}', '{detail_img_url}')""".format(
                    site_name=item['site_name'], domain=item['domain'], domain_url=item['domain_url'],
                    first_title=item['first_title'], first_title_url=item['first_title_url'],
                    second_title=item['second_title'],
                    second_title_url=item['second_title_url'], column_level=item['column_level'], price=2400,
                    title_detail=item['title_detail'], link_url=item['link_url'], img_url=item['img_url'],
                    compiler=item['compiler'], come_from=item['come_from'], release_time=item['release_time'],
                    content_detail=item['content_detail'], detail_img_url=item['detail_img_url'])
            elif spider.name == 'yokaClubColumn':
                insert_sql = """insert ignore into yoka_club_column_detail(site_name, domain, domain_url, 
                                first_title, first_title_url, second_title, second_title_url, column_level, 
                                price, title_detail, link_url, img_url, compiler, come_from, release_time, 
                                content_detail, detail_img_url) VALUES ('{site_name}', '{domain}', '{domain_url}', 
                                '{first_title}', '{first_title_url}', '{second_title}', '{second_title_url}', 
                                '{column_level}', '{price}', '{title_detail}', '{link_url}', '{img_url}', '{compiler}', 
                                '{come_from}', '{release_time}', '{content_detail}', '{detail_img_url}')""".format(
                    site_name=item['site_name'], domain=item['domain'], domain_url=item['domain_url'],
                    first_title=item['first_title'], first_title_url=item['first_title_url'],
                    second_title=item['second_title'],
                    second_title_url=item['second_title_url'], column_level=item['column_level'], price=2400,
                    title_detail=item['title_detail'], link_url=item['link_url'], img_url=item['img_url'],
                    compiler=item['compiler'], come_from=item['come_from'], release_time=item['release_time'],
                    content_detail=item['content_detail'], detail_img_url=item['detail_img_url'])
            else:
                insert_sql = ''
            # insert_sql = insert_sql.encode('gbk', 'ignore')
            # print(insert_sql)
            # print("item", item)
            self.cursor.execute(insert_sql)
            # 4. 提交操作
            self.connect.commit()
        except Exception as e:
            with open('error_beauty.txt', 'a') as f:
                f.write((str(item)) + '\n')
            print("YokaClubDetailPipeline.process_item:{}".format(e))

    def close_spider(self, spider):
        self.cursor.close()
        self.connect.close()


class YokaDetailPipelineJson(object):
    def open_spider(self, spider):
        # 1. 打开文件
        if spider.name == 'yokaClub':
            self.f = open('yokaClub.json', 'w', encoding='utf8')
        elif spider.name == 'yokaBeauty':
            self.f = open('yokaBeauty.json', 'w', encoding='utf8')
        elif spider.name == 'yokaHomePage':
            self.f = open('yokaHomePage.json', 'w', encoding='utf8')

    def process_item(self, item, spider):
        """将每一个Item数据交由该方法进行处理"""
        # 2. 写数据
        if spider.name in ['yokaClub', 'yokaBeauty', 'yokaHomePage']:
            # 将数据以json格式写入文件
            json.dump(dict(item), self.f, ensure_ascii=False)
            # 每一个条数据占一行
            self.f.write('\n')
        return item

    def close_spider(self, spider):
        if spider.name in ['yokaClub', 'yokaBeauty', 'yokaHomePage']:
            # 3. 关闭文件
            self.f.close()

        # class YokaBeautyDetailPipelineJson(object):
        #     def open_spider(self, spider):
        #         # 1. 打开文件
        #         if spider.name == 'yokaBeauty':
        #             self.f = open('yokaBeauty.json', 'w', encoding='utf8')
        #
        #     def process_item(self, item, spider):
        #         """将每一个Item数据交由该方法进行处理"""
        #         # 2. 写数据
        #         if spider.name == 'yokaBeauty':
        #             # 将数据以json格式写入文件
        #             json.dump(dict(item), self.f, ensure_ascii=False)
        #             # 每一个条数据占一行
        #             self.f.write('\n')
        #         return item
        #
        #     def close_spider(self, spider):
        #         if spider.name == 'yokaBeauty':
        #             # 3. 关闭文件
        #             self.f.close()

        # def get_map_price(self):
        #     """
        #     一级栏目名(板块名称)-二级栏目名(栏目名称)-栏目等级
        #     :return: 返回 dataframe 的深拷贝对象
        #     """
        #     from sqlalchemy import create_engine
        #     engine = create_engine("mysql+pymysql://|_|^spider^|_|:a19956171223@59.111.106.192/YokaDB?charset=utf8mb4")
        #     connection = engine.connect()
        #     sql = """select * from yoka_detail"""
        #     epaper_dpc_df = pd.read_sql(sql, connection)
        #     epaper_dpc_df = copy.deepcopy(epaper_dpc_df)
        #     print(epaper_dpc_df)
        #     connection.close()
        #     del connection
        #     return epaper_dpc_df
        value_dict = {
            # "value": dict(item),
            "sql": "INSERT INTO Epaper.epaper(domain,url,url_category,section,release_time,create_time,article_title) "
                   "VALUES (%(domain)s, %(url)s, %(url_category)s, %(section)s, %(release_time)s, %(create_time)s, %(article_title)s) "
                   "ON DUPLICATE KEY UPDATE domain=IF(domain!=VALUES(domain), VALUES(domain), domain), "
                   "url_category=IF(url_category!=VALUES(url_category), VALUES(url_category), url_category), "
                   "section=IF(section!=VALUES(section), VALUES(section), section), "
                   "release_time=IF(release_time!=VALUES(release_time), VALUES(release_time), release_time), "
                   "create_time=IF(create_time!=VALUES(create_time), VALUES(create_time), create_time), "
                   "article_title=IF(article_title!=VALUES(article_title), VALUES(article_title), article_title);"
            # "sql": "insert ignore into Epaper.epaper(domain,url,url_category,section,release_time,create_time,article_title) "
            #        "value (%(domain)s, %(url)s, %(url_category)s, %(section)s, %(release_time)s, %(create_time)s, %(article_title)s)"
        }
