 -*- coding:utf-8 -*-
import re
import requests
from bs4 import BeautifulSoup

url = "http://guba.eastmoney.com/news,601398,135492215.html"
# url = "http://guba.eastmoney.com/news,zssh000001,627042900.html"
# 获取机构研报的具体内容
#

def get_content(url):
    headers = {
        'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36",
        # 'Accept': "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        # 'Accept-Encoding': "gzip, deflate, sdch",
        # 'Accept-Language': "zh-CN,zh;q=0.8",
        }

    html = requests.get(url, headers=headers).content
    # try:
    #     content = html.decode('gb2312').encode("utf-8")
    # except Exception, e:
    #     content = html.decode('gb2312')
    #     print Exception, " encode:", e

    content = html
    soup = BeautifulSoup(content,"lxml")
    print content
    article = soup.find('div',class_ = 'stockcodec').find('p', style="line-height: 164.28%;").contents
    article = soup.find('div', class_='stockcodec').contents
    result = u""
    result = result + article[3].text

    # result = result + article[5].string
    # for i in range(6,len(article)-1):
    #     items = article[i].contents[0]
    #     if items != None:
    #         result = result + items.string

    # for each in article[3].contents:
    #     items = each.string
    #     if items != None:
    #         result = result + items
    comment = soup.findAll('div',class_ = 'zwlitext stockcodec')
    publish_date = soup.find('div', class_='zwfbtime').contents[-1].string

    temp = re.findall('\d+', publish_date, re.S)
    publish_date = temp[0] + "-" + temp[1] + "-" + temp[2]
    publish_date = publish_date.encode("ascii")

    commentres = u""
    for each in comment:
        try:
            comitems = each.contents
        except Exception, e:
            print Exception, " comment:", e
        for item in comitems:
            if item.string != None:
                commentres = commentres + item.string.strip()

        commentres = commentres + "@"
    # print commentres
        # com = ""
        # for j in range(len(tt)):
        #     com = com + str(tt[j])
        # print com

    return result,commentres,publish_date

get_content(url)