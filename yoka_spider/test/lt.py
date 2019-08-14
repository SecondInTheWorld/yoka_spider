# 爱丽丝和鲍勃一起玩游戏，他们轮流行动。爱丽丝先手开局。
# 最初，黑板上有一个数字 N 。在每个玩家的回合，玩家需要执行以下操作：
#
# 选出任一 x，满足 0 < x < N 且 N % x == 0 。
# 用 N - x 替换黑板上的数字 N 。
# 如果玩家无法执行这些操作，就会输掉游戏。
#
# 只有在爱丽丝在游戏中取得胜利时才返回 True，否则返回 false。假设两个玩家都以最佳状态参与游戏。
# 示例 1：
#
# 输入：2
# 输出：true
# 解释：爱丽丝选择 1，鲍勃无法进行操作。
# 示例 2：
#
# 输入：3
# 输出：false
# 解释：爱丽丝选择 1，鲍勃也选择 1，然后爱丽丝无法进行操作。
import datetime


class Solution(object):
    def reverseString(self, s):
        """
        :type s: List[str]
        :rtype: None Do not return anything, modify s in-place instead.
        """
        reverseList = []
        while len(s) > 0:
            reverseList.append(s[-1])
            s.remove(s[-1])
        print(reverseList)
        return reverseList


# s = ["h","e","l","l","o"]
# a = Solution()
# print(a.reverseString(s))

link = "http://www.yoka.com/fashion/model/2019/73/53044301101274.shtml"
split_list = link.split('/')
nowData = str(datetime.datetime.now())[0:10]
release_time = split_list[5] + '-' + split_list[6][:2] + '-' + split_list[6][2:]
item = release_time if release_time else nowData
# print(item)

a = ["cba", "daf", "ghi"]
# for i in list(zip(*a)):
#     print(i, type(i))
# print(*zip(a))


re = '2019春夏纽约时装周'
if '春夏' in re:
    print(222)


def ttt():
    try:
        # a = 2
        b = a / 0
        print('a/0')
    except Exception as e:
        print(e)

def try_test():
    print('1111111111111111')
    ttt()
    b = a / 0
    print('22222222')


try_test()
