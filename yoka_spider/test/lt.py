# -*- coding: utf-8 -*-
import datetime
import re

from yoka_spider.log import logger


class Solution(object):
    def findWords(self, words):
        """
        :type words: List[str]
        :rtype: List[str]
        """
        set1 = set('qwertyuiop')
        set2 = set('asdfghjkl')
        set3 = set('zxcvbnm')
        return [i for i in s if set(i.lower()) <= set1 or set(i.lower()) <= set2 or set(i.lower()) <= set3]


s = ["Hello", "Alaska", "Dad", "Peace"]
# a = Solution()
# print(a.findWords(s))
# res = "background:#000 url(http://p3.yokacdn.com/pic/YOKA/2019-01-25/U464P1TS1548411340_54313.jpg) no-repeat center top"
# regex = "url\(([\s\S]*?)\)"
# res1 = re.search(regex, res).group(1)
# print(res1)

st = "http://p3.yokacdn.com/pic/YOKA/2019-01-25/U464P1TS1548411340_54313.jpg"

item = {}

link = "http://www.yoka.com/fashion/windows/2019/0729/53104601101648.shtml"
link2 = "http://dolphin.yoka.com/c?z=yoka&la=0&si=124&cgdd=38&c=708&ci=122&or=268&l=2676&bg=2676&b=2705&u=http://www.yoka.com/fashion/popinfo/2019/0812/53129801101794.shtml"


def get_data(link):
    try:
        # 发布时间格式处理
        split_list = link.split('/')
        print(split_list)
        if split_list:
            release_time = split_list[5] + '-' + split_list[6][0:2] + '-' + split_list[6][2:4]
            url = release_time
            return release_time[0:7]
    except Exception as e:
        print('link_url', item['link_url'])
        print("item", item)
        with open('error_detail_url.txt', 'a') as f:
            f.write((str(item)) + '\n')
        print("get_release_time:{}".format(e))
        logger.info("get_release_time:{}".format(e))


print(get_data(link2))
# print(str(datetime.datetime.now())[0:7])

# insert
# ignore
# into
# yoka_club_detail(site_name, domain, domain_url,
#                  first_title, first_title_url, second_title, second_title_url, column_level,
#                  price, title_detail, link_url, img_url, compiler, come_from, release_time,
#                  content_detail, detail_img_url)
# VALUES( % {site_name}
# s
# ', '
# {domain}
# ', '
# {domain_url}
# ',
# '{first_title}', '{first_title_url}', '{second_title}', '{second_title_url}',
# '{column_level}', '{price}', '{title_detail}', '{link_url}', '{img_url}', '{compiler}',
# '{come_from}', '{release_time}', '{content_detail}', '{detail_img_url}')""".format(
#     site_name=item['site_name'], domain=item['domain'], domain_url=item['domain_url'],
#     first_title=item['first_title'], first_title_url=item['first_title_url'],
#     second_title=item['second_title'],
#     second_title_url=item['second_title_url'], column_level=item['column_level'], price=2400,
#     title_detail=item['title_detail'], link_url=item['link_url'], img_url=item['img_url'],
#     compiler=item['compiler'], come_from=item['come_from'], release_time=item['release_time'],
#     content_detail=item['content_detail'], detail_img_url=item['detail_img_url'])

a = 'abv'

l1 =[1,2]
l2 = [2,3]
l3=[4,5]
print(l1.extend(l2))
print(l1.extend(l3))
print(l1)
l4 = []
l4[0:7]
print(l4[0:7])
if l4[0:7] in l2:
    print(66666666)