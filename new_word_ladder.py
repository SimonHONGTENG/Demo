import re
from pprint import pprint

from var_dump import var_dump


def same(item, target):#返回两个单词相同字母的个数
    # var_dump([c for (c, t) in zip(item, target) if c == t])# test
    # var_dump(len([c for (c, t) in zip(item, target) if c == t]))# test
    return len([c for (c, t) in zip(item, target) if c == t])


def build(pattern, words, seen, list):#返回只相差一个字母的单词列表
    return [word for word in words if re.search(pattern, word) and word not in seen.keys() and word not in list]


def find(word, words, seen, target, path):
    if len(path) >= steps:#长度
        return True
    path = path.copy()
    list = []
    for i in range(len(word)):
        list += build(word[:i] + "." + word[i + 1:], words, seen, list)
    if len(list) == 0:
        return False

    list = sorted([(same(w, target), w) for w in list])#list保存了类似[(0,'lead'),...这样的东西
    list = sorted(list,key=lambda x:x[0], reverse=True) #修改
    for (match, item) in list:
        if match >= len(target) - 1:
            if match == len(target) - 1:
                path.append(item)#如果只相差一个单词就加入path
            path.append(target)
            print('->'.join(path))#修改
            return True
        seen[item] = True
    for (match, item) in list:
        path.append(item)
        if find(item, words, seen, target, path):
            # return True
            continue#修改
        path.pop()


# fname = input("Enter dictionary name: ")
fname = 'dictionary.txt'
file = open(fname)
lines = file.readlines()
steps = 6
while True:
    # start = input("Enter start word:")
    start = 'lead'
    words = []
    for line in lines:
        word = line.rstrip()
        if len(word) == len(start):
            words.append(word)
    # target = input("Enter target word:")
    target = 'gold'
    break

count = 0
path = [start]
seen = {start: True}
if find(start, words, seen, target, path):
    print(len(path) - 1, path)
else:
    print("No path found")
