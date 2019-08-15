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
res = "background:#000 url(http://p3.yokacdn.com/pic/YOKA/2019-01-25/U464P1TS1548411340_54313.jpg) no-repeat center top"
regex = "url\(([\s\S]*?)\)"
res1 = re.search(regex, res).group(1)
print(res1)

st = "http://p3.yokacdn.com/pic/YOKA/2019-01-25/U464P1TS1548411340_54313.jpg"

item = {}
def get_data(item):
    try:
        link = "http://www.yoka.com/fashion/model"
        split_list = link.split('/')
        nowData = str(datetime.datetime.now())[0:10]
        release_time = split_list[5] + '-' + split_list[6][:2] + '-' + split_list[6][2:]
        item['url'] = release_time if release_time else nowData
    except Exception as e:
        item['url'] = nowData
        print(e)
    print(item)
get_data(item)