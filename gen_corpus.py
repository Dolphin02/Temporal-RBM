# -*- coding: utf-8 -*-
from __future__ import print_function, unicode_literals
import re
import jieba
import jieba.posseg as pseg
import os
import sys
from sklearn import feature_extraction
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_extraction.text import CountVectorizer
import jieba.analyse
import random
import time
import MySQLdb
import numpy as np
import codecs
from DB_connection import DBUtil
# 连接数据库获取股票研报content和title
def get_content():
    try:
        info = DBUtil.select_datas("select * from news where id >= 20000 and id < 40000;")# flag = 运行guo
        res = []
        for each in info:
            res.append(each)
        return res
    except Exception as e:
        print (Exception, ":", e)


def dealDict(file):
    try:
        fileread = open(file, 'r')
        line = fileread.readline()
        s = type(line)
        result = []
        while line:
            line = line.decode("utf-8")
            m = type(line)

            linetemp = line.replace("\r", "").replace("\n", "").replace("\t", "")
            linetemp = linetemp.replace(u'\xa0', u'')
            linetemp.encode("utf-8")
            result.append(linetemp)
            # for i in range(length):
            #     temp = line[i]
            #     print(temp)
            line = fileread.readline()
            # print each
        fileread.close()
        result.append(" ")
        return result
    except Exception, e:
        print(Exception, ":", e)

# stopDict = get_stopDict()


def dealStockDict(file):
    try:
        fileread = open(file, 'r')
        #filewrite = open("stockDict.txt", 'w')
        filewrite = codecs.open("stockDict.txt", 'a', 'utf-8')
        line = fileread.readline()
        s = type(line)
        result = []
        while line:

            m = type(line)
            linetemp = line.decode("utf-8")
            #linetemp = line.replace("\r", "").replace("\n", "").replace("\t", "")
            # linetemp = linetemp.replace(u'\xa0', u'')
            #linetemp = line.replace(u'\xa0', u'')

            #print(linetemp)
            filewrite.write(linetemp)
            result.append(linetemp)
            # for i in range(length):
            #     temp = line[i]
            #     print(temp)
            line = fileread.readline()
            # print each
        fileread.close()
        filewrite.close()
        result.append(" ")
        return result
    except Exception, e:
        print(Exception, ":", e)

stopwords = {}.fromkeys([line.decode('utf-8').rstrip() for line in open('lexicon/stopDict.txt')])  # 加载停用词字典
jieba.load_userdict("lexicon/stockDict.txt")


def get_sentimentDict(filename):
    fileread = open(filename, "r")
    word = []
    label = []

    line = fileread.readline()
    while line:
        word.append(line[:-3])
        label.append(line[-2])
        line = fileread.readline()
    fileread.close()
    return word, label


def gen_split_words():
    info = get_content()
    datas = np.array(info)
    # publish_date = datas[:, 2]
    titles = datas[:, 5]
    contents = datas[:, 7]
    # comments = datas[:, 8]
    res = []

    file = codecs.open("data//corpus.txt", 'a', 'utf-8')

    for each in contents:
        each = each.decode('utf-8')
        each = each.replace("\r", "").replace("\n", "").replace("\t", "").replace(" ","")
        if len(each) > 20:
            each = re.sub("[C-Za-z0-9\[\`\~\!\@\#\$\^\&\*\(\)\=\|\{\}\'\:\;\'\,\[\]\.\<\>\/\?\~\！\@\#\\\&\*\%\，\、\“\”\-\：\《\》\（\）]","", each)
            item = ""
            segs = jieba.lcut(each)
            for seg in segs:
                if seg not in stopwords and len(seg) > 0:
                    item = item + seg + " "
            res.append(item)
            file.write(item)
            print(item)

    for each in titles:
        each = each.decode("utf-8")
        each = re.sub( "[\[\`\~\!\@\#\$\^\&\*\(\)\=\|\{\}\'\:\;\'\,\[\]\.\<\>\/\?\~\！\@\#\\\&\*\%\，\、\“\”\-\：\《\》\（\）]","", each)
        each = each.replace("\r", "").replace("\n", "").replace("\t", "").replace(" ", "")
        item = ""
        segs = jieba.lcut(each)
        for seg in segs:
            # if seg in stopwords:
            #     tt = seg
            #     print(seg)
            if seg not in stopwords and len(seg) > 0:
                item = item + seg + " "
        res.append(item)
        file.write(item)
        print(item)

    # for each in comments:
    #     each = each.decode("utf-8")
    #     each = re.sub( "[A-Za-z0-9\[\`\~\!\@\#\$\^\&\*\(\)\=\|\{\}\'\:\;\'\,\[\]\.\<\>\/\?\~\！\@\#\\\&\*\%\，\、\“\”\-\：\《\》\（\）]","", each)
    #     each = each.replace("\r", "").replace("\n", "").replace("\t", "").replace(" ", "")
    #     item = ""
    #     segs = jieba.lcut(each)
    #     for seg in segs:
    #         if seg not in stopwords and len(seg) > 0:
    #             item = item + seg + " "
    #     res.append(item)
    #     file.write(item)
    #     print(item)
    return res

gen_split_words()















def get_sentimentDict(filename):
    fileread = open(filename,"r")
    word = []
    label = []

    line = fileread.readline()
    while line:
        word.append(line[:-3])
        label.append(line[-2])
        line = fileread.readline()
    fileread.close()
    return word,label





def output(weights, words, id):
    score = 0
    weight_index_sort = np.argsort(-weights)
    filename = "no" + str(id + 1) + "TF-IDF.txt"
    # file = open(filename, "w")
    file = codecs.open(filename, 'w', 'utf-8')
    for i in range(len(weights)):
        word = words[weight_index_sort[i]]
        weight = weights[weight_index_sort[i]]
        if weight > 0:
            temp = words[weight_index_sort[i]] + "   " + str(weights[weight_index_sort[i]]) + "\n"
            #file.write(temp)
            #print (words[weight_index_sort[i]], weight[weight_index_sort[i]])
            sentimentwords, labels = get_sentimentDict("lexicon//new.txt")
            for i in range(len(sentimentwords)):
                if sentimentwords[i].decode("utf-8") == word:
                    if labels[i] == "N":
                        score = score + weight*(-1)
                    elif labels[i] == "P":
                        score = score + weight

    file.close()
    #print (score)
    return score










