#!/usr/bin/python
# -*- coding: UTF-8 -*-


tree1 = ["这", ["是",["this","is"]], "一个", "测试"]

#递归函数
def look(tree):
    for i in tree:
        if type(i)==str:
            print(i)
        else:
            look(i)

look(tree1)
