# -*- coding:utf-8 -*-

"""
|   @project : ourui_sql_acceptance
|   @author  : chencheng
|   @file    : michenlin_clone
|   @ide     : PyCharm
|   @time    : 2019-07-16 09:43:54
|   @describe

"""

import hashlib, re, time, requests, json, traceback
from pymysql import *
from datetime import datetime
from pymysql.err import OperationalError, IntegrityError
# from ourui_mq.mq_sender import MQSender
#
# ma_sender = MQSender()


# mysql 重连
def try_mysql_connect(func):
    def except_mysql_connect(self, sql):
        # mysql的连接出现异常
        try:
            if self.conn.open:
                return func(self, sql)
        except OperationalError:
            # 进行 mysql 重新连接
            if not self.conn.open:
                self.conn.ping(reconnect=True)
            if self.conn.open:
                return func(self, sql)
            else:
                print('he mysql link was closed')
        except IntegrityError:
            error_data = traceback.format_exc()
            print(error_data)
    return except_mysql_connect


class Michelin(object):
    def __new__(cls, **kwargs):
        if not hasattr(cls, 'instance'):
            cls.instance = super(Michelin, cls).__new__(cls)
        return cls.instance

    def __init__(self, **kwargs):
        self.conn = connect(
            host='59.111.106.192',
            port=3306,
            database='',
            user='|_|^spider^|_|',
            password='a19956171223',
            charset='utf8mb4',
            cursorclass=cursors.DictCursor)
        self.csl = self.conn.cursor()

    @try_mysql_connect
    def save_to_mysql(self, value_dict):
        """
        提交dict参数, 与 sql 语句 value 键名对应
        m = Michelin()
        value_dict = {"value": {"name": "1"},
                      "sql": "insert ignore into test_tables(a) value (%(name)s)"
                      }
        m.save_to_mysql(value_dict)

        :param sql: insert into table (key1, key2) value (%(value1)s, %(value2)s)
        :param value_dict: value 关键字名称对应 {"value1":"1", "value2":"2"}
        :return:
        """

        sql = value_dict.get('sql')
        value = value_dict.get('value')
        if sql and value:
            self.csl.execute(sql, value)
            self.conn.commit()