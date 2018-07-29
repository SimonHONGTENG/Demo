import re
import time
from pprint import pprint

from var_dump import var_dump


def isInDictory(s):
    isError = True
    for w in lines:
        w = w.rstrip()
        if s == w:
            isError = False
            break
    return isError


def checkWord(s):
    try:
        for i in s:
            if not ((65 <= ord(i) <= 90) or (97 <= ord(i) <= 122)):
                return True
        return False
    except:
        return True


def same(item, target):  # 返回两个单词相同字母的个数
    return len([c for (c, t) in zip(item, target) if c == t])


def build(pattern, words, seen, list, me):  # 返回只相差一个字母的单词列表
    l = []
    for word in words:
        if word == me:
            continue
        if re.search(pattern, word):
            if word not in path:
                if word not in list:
                    l.append(word)
    return l
    # return [word for word in words if re.search(pattern, word) and word not in seen.keys() and word not in list]


def find(word, words, seen, target, path):
    path = path.copy()
    if len(path) > steps:  # 长度
        return True
    path.append(word)
    list = []
    if word == target:
        print('->'.join(path))
        return True
    for i in range(len(word)):
        list += build(word[:i] + "." + word[i + 1:], words, seen, list, word)
    if len(list) == 0:
        return False

    list = sorted([(same(w, target), w) for w in list])  # list保存了类似[(0,'lead'),...这样的东西
    list = sorted(list, key=lambda x: x[0], reverse=True)  # 修改
    # print('-' * 10)
    # print(word, '::')
    # print('seen:', seen)
    # print('list:', len(list), list)
    # print('path', path, '\n')
    # 这里算法有严重问题
    # for (match, item) in list:
    #     if match >= len(target) - 1:
    #         if match == len(target) - 1:
    #             path.append(item)
    #         path.append(target)
    #         print('->'.join(path))
    #         return True
    #     seen[item] = True
    for (match, item) in list:
        find(item, words, seen, target, path)


cannotUse = []
while 1:
    # fname = input('输入字典文件:')
    # start = input('输入开始单词:')
    # target = input('输入结束单词:')
    # steps = int(input('输入步数:'))

    fname = 'dictionary.txt'
    start = 'lead'
    target = 'gold'
    steps = 4

    lent = len(target)
    try:
        file = open(fname)
    except:
        print('文件打开失败，请重新输入\n')
        continue
    if len(start) != len(target):
        print("开始单词和结束单词长度不等，请重新输入\n")
        continue
    if checkWord(start) or checkWord(target):
        print("单词含有非法字符，请重新输入\n")
        continue
    lines = file.readlines()
    if isInDictory(start):
        print(start + " 不在字典中，请重新输入\n")
        continue
    if isInDictory(target):
        print(target + " 不在字典中，请重新输入\n")
        continue
    # if input('你想限制某些单词不能在路径中使用么？ (y/n) :') == 'y':
    #     while 1:
    #         i = input('输入单词，输入-1退出输入 :')
    #         if i != '-1':
    #             if not checkWord(i):
    #                 cannotUse.append(i)
    #             else:
    #                 print('这好像不是一个单词')
    #         else:
    #             break
    print('输入正确，开始计算...')
    time_start = time.time()
    break
while True:
    words = []
    for line in lines:
        word = line.rstrip()
        if word in cannotUse: continue
        if len(word) == len(start):
            words.append(word)
    break

count = 0
# path = [start]
path = []  # 不能一开始就加
seen = {start: True}
if find(start, words, seen, target, path):
    print(len(path) - 1, path)
else:
    pass

print('耗时：', time.time() - time_start)
