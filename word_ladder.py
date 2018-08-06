import re
import time


def isDifferOne(a, b):#返回a,b是否只相差一个单词
    diff = 0#初始化相差0
    for i in range(len(a)):
        if a[i] != b[i]:#如果不一样
            if diff != 1:#而且不等于1
                diff += 1#就加以
            else:#否则就相差好多个 直接不循环了 返回 False
                return False
    return True# 不考虑 是否和自己 比较 seen中有自己 build0 的第二个循环会删掉在seen中出现的单词


def same(item, target):#返回和item 和 target 一样的字母个数
    return len([c for (c, t) in zip(item, target) if c == t])


def build(pattern, words, seen, list):#不使用的方法 效率极低
    return [word for word in words
            if re.search(pattern, word) and word not in seen.keys() and
            word not in list]


def build0(word, words, seen):#返回 和word 只差一个字母的list seen中 用过的不要
    l = []
    for i in words:
        if isDifferOne(word, i):#判断是否只差一个单词
            l.append(i)
    for i in l:
        if i in seen:#seen中 用过的不要
            l.remove(i)
    return l


def find(word, words, seen, target, path):#递归找路径 实际上是 有向图求最短路径问题 这里用的是 Dijkstra 算法 文字讲不清楚 具体的百度下 就会很明白
    seen = seen.copy()#复制下 否则 子节点用过的 父节点的 兄弟结点用不了 但是要用这个 必然会有 父节点 和 父节点的兄弟节点 都 有 同一个只差一个字母的单词 但是父节点用了 其兄弟结点就没法用 所以会缺少路径
    global paths
    path = path.copy()#path 也是一个道理 用过的在下面不能用了 否则死循环
    if word in path:#用过的 不能用
        return
    if len(path) > steps:  # 太长了 我们要的是 指定长度的 比如3 步
        return
    path.append(word)#加到路径里

    if word == target:#单词和目标词一样 就找到了
        global time_start#时间
        print('Find a path step=', len(path) - 1, '->'.join(path), time.time() - time_start)#输出
        time_start = time.time()#重置时间
        paths.append(path)#加到paths里
        return#不用循环了 已经找到了
    # for i in range(len(word)):
    #     list += build(word[:i] + "." + word[i + 1:], words, seen, list)
    list = build0(word, words, seen)#上面注释掉的两行和这行功能一样 但是 build0 效率更高
    if len(list) == 0:#没有he word 只差一个字母的单词 那就返回
        return False

    list = sorted([(same(w, target), w) for w in list])  # list保存了类似[(0,'lead',1,'hide'),...这样的东西 前面的数字代表了和target 有几个相同的字母 就相当于 权
    list = sorted(list, key=lambda x: x[0], reverse=True)  # 从大到小 大的先遍历

    for (match, item) in list:#下面四行不需要 上面 if word == target: 已经代替了他的功能 如果 这样的慌=话 会少很多很多结果 因为 他return 了 list 中可能有其他单词也能找到路径
        # if match >= len(target) - 1:
        #     if match == len(target) - 1:
        #         path.append(item)
        #     return True
        seen[item] = True#加到考察列表里去
    # for (match, item) in list:
    #     path.append(item)
    #     if find(item, words, seen, target, path):
    #         return True
    #     path.pop()

    for (match, item) in list:#根据权重来 先循环的 是 和 target 相同单词多的 这样更容易找到 这也是 Dijkstra 算法 的核心思想
        find(item, words, seen, target, path)#递归


def isInDictionary(s):  # 是不是在字典里
    isError = True  # 默认不是
    for w in lines:  # 每个取出来比较
        w = w.rstrip()  # 去换行符
        if s == w:  # 找到了 才设置为是
            isError = False
            break
    return isError


def checkWord(s):  # 检查是不是单词
    try:
        for i in s:
            if not ((65 <= ord(i) <= 90) or (97 <= ord(i) <= 122)):  # ascii a-z 和 A-Z 的范围
                return True
        return False
    except:
        return True


def userInput():  # 用户输入
    global fname  # 必须用全局 否则改不了
    global start
    global target
    global steps
    global cannotUse
    global shortist
    fname = input('输入字典文件:')  # 括号里为提示语句
    start = input('输入开始单词:')
    target = input('输入结束单词:')
    steps = input('输入步数:')
    if input('你想限制某些单词不能在路径中使用么？ (y/n) :') == 'y':  # 设置不能用的单词
        while 1:
            i = input('输入单词，输入-1退出输入 :')
            if i != '-1':  # 不是-1 储存
                if not checkWord(i):  # 必须是单词才行
                    cannotUse.append(i)
                else:
                    print('这好像不是一个单词')
            else:  # 否则 结束循环
                break
    if input('你想在最后展示最短路径么？ (y/n) :') == 'y':  # 是否展示最短路径
        shortist = True


def checkUserInput():  # 检查用户输入的内容
    global steps  # 全局变量 方便修改
    global lines  # 全局变量 方便修改
    try:
        try:  # 文件操作出错 直接 return False
            file = open(fname)  # 打开文件
            lines = file.readlines()  # 读文件
            file.close()  # 关闭文件
        except:  # 捕获到错误
            print('文件打开失败，请重新输入\n')  # 提示
            return False
        if len(start) != len(target):  # 长度不等的不行
            print("开始单词和结束单词长度不等，请重新输入\n")
            return False
        if checkWord(start) or checkWord(target):  # 单词只能有字母，其他一律不行
            print("单词含有非法字符，请重新输入\n")
            return False
        if isInDictionary(start):  # 单词不在字典里不行
            print(start + " 不在字典中，请重新输入\n")
            return False
        if isInDictionary(target):  # 单词不在字典里不行
            print(target + " 不在字典中，请重新输入\n")
            return False
        steps = int(steps)  # 变成整型
        return True
    except:  # 捕获到意料之外的错误，直接return False
        print('输入错误，请重新输入\n')
        return False


def findWords():  # 将从文件中读取的每行内容满足和start长度相同的放进去，但是不包括用户指定的不需要的单词
    global words  # 全局变量
    for line in lines:
        word = line.rstrip()  # 去除换行符 \n
        if len(word) == len(start):  # 满足条件的
            if word in cannotUse:  # 去掉不用的
                continue  # 继续循环
            words.append(word)  # 加进去


def getShortist(l):  # l 为像这样的列表 [[1, 2, 3], [1, 2], [1, 2, 3, 4, 5]]), [1, [[1, 2]]] 但是其中是单词而不是数字
    minLen = -1  # 最短路径长度
    shorts = []  # 满足长度的许多路径
    for i in l:  # 循环取出来
        if len(i) < minLen or minLen == -1:  # 碰到更短的长度 或 minlen 没被赋值时
            minLen = len(i)  # 就赋值
    for i in l:  # 循环取出
        if len(i) == minLen:  # 长度满足的
            shorts.append(i)  # 放进去
    return [minLen - 1, shorts]  # 返回 长度减1，因为steps和长度差1，和返回列表


time_start = time.time()  # 当前时间
fname = 'dictionary.txt'  # 文件路径
start = 'lead'  # 开始单词
target = 'gold'  # 结束单词
steps = 3  # 搜索最大深度，如果不设置，会有无数种路径
lines = []  # 从文件中读取的每一行存在这个list里
cannotUse = []  # 用户指定的不能使用的单词
shortist = True  # 是否展示最短路径
path = []  # 一条路径
paths = []  # 很多路径
seen = {start: True}  # 用过的单词
words = []  # 剔除了和start 单词长度不同和不允许使用单词的剩下的单词
if __name__ == '__main__':  # 只有在运行这个py文件时才为True,在测试脚本不会运行下面代码
    # userInput()  # 用户输入
    while not checkUserInput():  # 检查输入是否有错 有错就重新输入
        userInput()  # 有错 再次输入
    time_start = time.time()  # 重新开始计时
    findWords()  # 把单词存在words中
    find(start, words, seen, target, path)  # 开始寻找路径
    if len(paths) != 0:  # 当路径条数不为0时
        if shortist:  # 当用户开始 回答 "你想在最后展示最短路径么？ (y/n) :" 为 y 时
            x, y = getShortist(paths)  # 返回最短路径的 长度 和 这个长度的所有路径
            print('-' * 40)  # 输出40个-
            print('\t' * 3, '计算结果')  # 输出          计算结果
            print('一共找到路径：', len(paths))  # 输出 一共找到路径
            print('最短的路径长度为：', x, " 有：", len(y), '条')  # 输出 最短的路径长度为  有  条
            print('下面是最短的路径：')  # 输出 下面是最短的路径：
            for i in y:  # 循环取出每一条
                print('->'.join(i))  # 用 -> 为分隔符 将路径单词构成一个字符串
            print('_' * 40)  # 输出40个_
    else:  # 否则
        print('没找到路径')  # 输出没找到路径
    print('总耗时：', time.time() - time_start)  # 输出总消耗的时间
