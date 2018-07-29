import re
import time


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


def build(pattern, words, list, me):  # 返回只相差一个字母的单词列表
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


def find(word, words, target, path):
    global paths
    path = path.copy()
    if len(path) > steps:  # 长度
        return
    path.append(word)
    list = []
    if word == target:
        print('Find a path step=', len(path), '->'.join(path))
        paths.append(path)
        return
    for i in range(len(word)):
        list += build(word[:i] + "." + word[i + 1:], words, list, word)
    if len(list) == 0:
        return
    list = sorted([(same(w, target), w) for w in list])  # list保存了类似[(0,'lead'),...这样的东西
    list = sorted(list, key=lambda x: x[0], reverse=True)  # 修改
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
        find(item, words, target, path)


def userInput():
    global fname
    global start
    global target
    global steps
    global lent
    global file
    global lines
    global cannotUse
    global shortist
    while 1:
        try:
            # fname = input('输入字典文件:')
            # start = input('输入开始单词:')
            # target = input('输入结束单词:')
            # steps = int(input('输入步数:'))

            fname = 'dictionary.txt'
            start = 'lead'
            target = 'gold'
            steps = 3

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
            if input('你想限制某些单词不能在路径中使用么？ (y/n) :') == 'y':
                while 1:
                    i = input('输入单词，输入-1退出输入 :')
                    if i != '-1':
                        if not checkWord(i):
                            cannotUse.append(i)
                        else:
                            print('这好像不是一个单词')
                    else:
                        break
            if input('你想在最后展示最短路径么？ (y/n) :') == 'y':
                shortist = True
            return 'ok'
        except:
            print('输入错误，，请重新输入\n')
            continue


def getShortist(l):
    minLen = -1
    shorts = []
    for i in l:
        if len(i) < minLen or minLen == -1:
            minLen = len(i)
    for i in l:
        if len(i) == minLen:
            shorts.append(i)
    return [minLen, shorts]


time_start = time.time()
fname = ''
start = ''
target = ''
steps = 0
lent = 0
lines = []
cannotUse = []
words = []
shortist = False
path = []
paths = []
if userInput() == 'ok':
    print('输入正确,开始计算...')
else:
    print('error')
    userInput()
for line in lines:
    word = line.rstrip()
    if word in cannotUse: continue
    if len(word) == len(start):
        words.append(word)
find(start, words, target, path)
if len(paths) != 0:
    if shortist:
        x, y = getShortist(paths)
        print('-' * 40)
        print('\t' * 3, '计算结果')
        print('一共找到路径：', len(paths))
        print('最短的路径长度为：', x, " 有：", len(y), '条')
        print('下面是最短的路径：')
        for i in y:
            print('->'.join(i))
        print('*' * 40)
else:
    print('没找到路径')

print('总耗时：', time.time() - time_start)
