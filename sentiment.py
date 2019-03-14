# # -*- coding: utf-8 -*-
# from __future__ import print_function, unicode_literals
# import re
# import jieba
# import jieba.posseg as pseg
# import os
# import sys
# from sklearn import feature_extraction
# from sklearn.feature_extraction.text import TfidfTransformer
# from sklearn.feature_extraction.text import CountVectorizer
# import jieba.analyse
# import random
# import time
# import MySQLdb
# import numpy as np
# import codecs
#
# def dealDict(file):
#     try:
#         fileread = open(file, 'r')
#         line = fileread.readline()
#         result = []
#         while line:
#             line = line.decode("utf-8")
#             linetemp = line.replace("\r", "").replace("\n", "").replace("\t", "")
#             linetemp = linetemp.replace(u'\xa0', u'')
#             linetemp.encode("utf-8")
#             result.append(linetemp)
#             line = fileread.readline()
#         fileread.close()
#         result.append(" ")
#         return result
#     except Exception, e:
#         print(Exception, ":", e)
#
# def get_content(path):
#     file_reader = open(path, "r")
#     line = file_reader.readline()
#     stopDict = dealDict('lexicon//stopDict.txt')   # 停用词词典
#     posDict = dealDict('lexicon//positive.txt')  # 积极的情感词典
#     negDict = dealDict('lexicon//negative.txt')  # 消极的情感词典
#     negatiDict = dealDict('lexicon//negaDict.txt')  # 否定词词典
#     stopwords = {}.fromkeys(stopDict)
#     negatiWords = {}.fromkeys(negatiDict)
#     posWords = {}.fromkeys(posDict)
#     negWords = {}.fromkeys(negDict)
#     corpus = []
#     while line:
#        line = line.decode("utf-8")
#        text = re.sub("[A-Za-z0-9\[\`\~\!\@\#\$\^\&\*\(\)\=\|\{\}\'\:\;\'\,\[\]\.\<\>\/\?\~\！\@\#\\\&\*\%]", "",line)
#        jieba.load_userdict("lexicon//stockDict.txt")
#        tags = jieba.lcut(text, cut_all=False)
#        All = ""
#        for each in tags:
#             # each.encode("utf-8")
#             if each not in stopwords:
#                  if each in posWords:
#
#                  All = All + each + " "
#                 # print("导入后关键词抽取:", "/".join(All))
#        line = file_reader.readline()
#
# # 对content和title进行分割，提取关键词
# def get_cutContent():
#     stopDict = dealDict('stopDict.txt')
#     stopwords = {}.fromkeys(stopDict)
#
#     #stockWords = dealDict("stockDict.txt")
#     corpus = []
#     for i in range(len(content)):
#         temp = content[i].decode("utf-8")
#         temp = re.sub("[A-Za-z0-9\[\`\~\!\@\#\$\^\&\*\(\)\=\|\{\}\'\:\;\'\,\[\]\.\<\>\/\?\~\！\@\#\\\&\*\%]", "", temp)
#         # tags = jieba.lcut(temp, cut_all=False)
#         # print("关键词抽取:", "/".join(tags))
#         jieba.load_userdict("stockDict.txt")
#         tags = jieba.lcut(temp, cut_all=False)
#         All = ""
#         for each in tags:
#             #each.encode("utf-8")
#             if each not in stopwords:
#                 All = All + each + " "
#     # print("导入后关键词抽取:", "/".join(All))
#         corpus.append(All)
#     return corpus
#
#
#
#
# # 处理情感词典的词
# def deal_sentimentDict(filename):
#     try:
#         fileread = codecs.open(filename,"r",'utf-8')
#         line = fileread.readline()
#         result = []
#         while line:
#             line = line
#             linetemp = line.replace("\r", "").replace("\n", "").replace("\t", "")
#             linetemp = linetemp.replace(u'\xa0', u'')
#             linetemp.encode("utf-8")
#             result.append(linetemp)
#             line = fileread.readline()
#         fileread.close()
#         return result
#     except Exception, e:
#         print(Exception, ":", e)
#
# def get_sentimentDict(filename):
#     fileread = codecs.open(filename,"r",'utf-8')
#     word = []
#     label = []
#
#     line = fileread.readline()
#     while line:
#         word.append(line[:-3])
#         label.append(line[-2])
#         line = fileread.readline()
#     fileread.close()
#     return word,label
#
#
#
# # def cal_sentiment(words):
# #     # posDict = codecs.open('lexicon/positive.txt', 'r', 'utf-8')
# #     # negDict = codecs.open('lexicon/negative.txt', 'r', 'utf-8')
# #
# #     #sentimentwords, labels = get_sentimentDict("lexicon/new.txt")
# #     n = len(words)
# #     neg = []
# #     pos = []
# #     for i in range(n):
# #         n = 0.0
# #         p = 0.0
# #         for each in words[i]:
# #             word = each.split('/')[0]
# #             if word in posWords:
# #                 n = n + (-1)
# #                 # print(word)
# #             elif word in negWords:
# #                 p = p + 1
# #                 # print(word)
# #             # for k in range(len(labels)):
# #
# #                 # if sentimentwords[k] == word:
# #                 #     if int(labels[k]) == -1:
# #                 #         print ('66')
# #                 #         n = n + (-1)
# #                 #     elif labels[k] == "1":
# #                 #         p = p + 1
# #         if -n+p != 0:
# #             n = (n*1.0/(-n+p))
# #             p = (p*1.0/(-n+p))
# #         neg.append(n)
# #         pos.append(p)
# #     return neg,pos
#
# def deal_adv():
#     reader = codecs.open('lexicon/adv.txt', 'r', 'utf-8')
#     line = reader.readline()
#     advDict = {}
#     while line:
#         tokens = line[:-1].split(' ')
#         advDict[tokens[0]] = tokens[1].encode('utf-8')
#         line = reader.readline()
#     return advDict
#
# # def cal_sentiment_multi(contents):  # 加入否定词、程度副词之后，对情感值进行计算
# #     # posDict = codecs.open('lexicon/positive.txt', 'r', 'utf-8')
# #     # negDict = codecs.open('lexicon/negative.txt', 'r', 'utf-8')
# #
# #     #sentimentwords, labels = get_sentimentDict("lexicon/new.txt")
# #     advDict = deal_adv()
# #     n = len(contents)
# #     scores = []
# #     for i in range(n):
# #         count = 0.0
# #         score = 0
# #         sentence = contents[i]
# #         for k in range(len(sentence)):
# #             word = sentence[k].split('/')[0]  # 文本切分结果包含词性标注，只取词语
# #             if word in posWords:     # 积极词语
# #                 count += 1
# #                 if k > 0:           # 积极词语存在前一词语
# #                     front = sentence[k-1].split('/')[0]  # 前一词语
# #                     if front in negWords or front in negatiWords:
# #                         score = score - 1
# #                     if front in advDict:
# #                         score = score + 1 + float(advDict[front])
# #                     else:
# #                         score = score + 1
# #                 else:
# #                     score = score + 1
# #
# #                 if k < len(sentence) - 1:# 积极词语存在后一词语
# #                     next = sentence[k + 1].split('/')[0]  # 后一词语
# #                     if next in negWords:
# #                         score = score - 1
# #                     else:
# #                         score = score + 1
# #                 else:
# #                     score = score + 1
# #                 # print(word)
# #             elif word in negWords:
# #                 count += 1
# #                 if k > 0:           # 消极词语存在前一词语
# #                     front = sentence[k-1].split('/')[0]  # 前一词语
# #                     if  front in negatiWords:
# #                         score = score + 1
# #                     if front in advDict:
# #                         score = score - 1 - float(advDict[front])
# #                     else:
# #                         score = score - 1
# #                 else:
# #                     score = score - 1
# #
# #         if count != 0:
# #             scores.append(score/count)
# #         else:
# #             scores.append(0.0)
# #     return scores
#
#
# def output(weights, words, id):
#     neg_score = 0
#     pos_score = 0
#     score = 0
#     weight_index_sort = np.argsort(-weights)
#     filename = "no" + str(id + 1) + "TF-IDF.txt"
#     # file = open(filename, "w")
#     # file = codecs.open(filename, 'w', 'utf-8')
#     for i in range(len(weights)):
#         word = words[weight_index_sort[i]]
#         weight = weights[weight_index_sort[i]]
#         if weight > 0:
#             temp = words[weight_index_sort[i]] + "   " + str(weights[weight_index_sort[i]]) + "\n"
#             # file.write(temp)
#             #print (words[weight_index_sort[i]], weight[weight_index_sort[i]])
#             sentimentwords, labels = get_sentimentDict("new.txt")
#             for i in range(len(sentimentwords)):
#                 if sentimentwords[i].decode("utf-8") == word:
#                     if labels[i] == "N":
#                         score = score + (-1)
#                     elif labels[i] == "P":
#                         score = score + 1
#
#     file.close()
#     print (score)
#     return score
#
#
#
# text_type = ["forum", "report", "news", "notice"]
# part_path = "C://Users//Dolphin//Desktop//stockdate//11//"
# for type in text_type:
#     path = part_path + type + ".txt"
#     get_content(path)
#     index, content, labels, publish_date = get_content(path)
#     scores = cal_sentiment_multi(content)
#     i = 0
#     while line:
#         temp = publish_date[i] + '\t' + "%.4f" % (scores[i])
#         line = reader.readline()
#         i = i + 1
#     reader.close()
#
#
#
