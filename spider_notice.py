# -*-coding:utf-8 -*-
import urllib2
from lxml import etree
from bs4 import BeautifulSoup
from datetime import date
import MySQLdb
import requests
import re
import json
import time
import random
import datetime
import sys
reload(sys)
sys.setdefaultencoding('utf8')
# 获取每一页的URL,返回URL列表
def get_pageUrl(start,n,stockid):
    tempurl = 'http://guba.eastmoney.com/list,' + stockid + ',3,f_'
    urls = []
    for page in range(start,n+1):
        urls.append(tempurl + str(page)+".html")
    return urls


#url = "http://js4.eastmoney.com/count.aspx?unit_id=emcount&ck=34332052573139921851&cookie_rndnum_new=0&ade=0&adtm=0&sttm=0&ss=1740857024&uvt=0&co_enabled=1&UrlReferrer=http%3A//guba.eastmoney.com/list%2Cszzs_4046.html&urlCurrent=http%3A//guba.eastmoney.com/list%2Cszzs_1.html&dom=eastmoney.com&dom_charcode=1346&lock_flag=0&nvapp=Netscape&agt=Mozilla/5.0%20%28Windows%20NT%2010.0%3B%20Win64%3B%20x64%29%20AppleWebKit/537.36%20%28KHTML%2C%20like%20Gecko%29%20Chrome/57.0.2987.133%20Safari/537.36&clr=24-bit&scr=1920x1080&lng=zh-cn&jve=0&flv=25.0%20r0&cpyno=c1&rndnum=0.5621341972615888"
# 获取机构研报的所有内容
def get_infoJson(url):
    headers = {
    'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.79 Safari/537.36 Edge/14.14393",
    }
    html = requests.get(url, headers=headers)
    data = html.content
    return data



# url = "http://guba.eastmoney.com/news,zssh000001,627042900.html"
# 获取机构研报的具体内容

def get_content(url):
    headers = {
        'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.79 Safari/537.36 Edge/14.14393",
        'Accept': "application/json, text/javascript, */*; q=0.01",
        'Accept-Encoding': "gzip, deflate, sdch",
        'Accept-Language': "zh-CN,zh;q=0.8",
        }

    html = requests.get(url, headers=headers).content
    # try:
    #     content = html.decode('gb2312').encode("utf-8")
    # except Exception, e:
    #     content = html.decode('gb2312')
    #     print Exception, " encode:", e

    content = html
    soup = BeautifulSoup(content,"lxml")
    #print soup
    # article = soup.find('div',class_ = 'stockcodec').find('p', style="line-height: 164.28%;").contents
    article = soup.find('div', class_='stockcodec').contents
    result = u""
    for each in article[3].contents:
        items = each.string
        if items != None:
            result = result + items
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

def get_content1(url):
    headers = {
         'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36",
        # 'Accept': "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        }

    html = requests.get(url, headers=headers).content
    # try:
    #     content = html.decode('gb2312').encode("utf-8")
    # except Exception, e:
    #     content = html.decode('gb2312')
    #     print Exception, " encode:", e

    content = html
    soup = BeautifulSoup(content,"lxml")
    #print soup
    # article = soup.find('div',class_ = 'stockcodec').find('p', style="line-height: 164.28%;").contents
    try:
        article = soup.find('div', class_='stockcodec').find('div', id='zw_body').contents
        try:
            result = u""
            result = result + article[0].text
        except Exception, e:
            article = soup.find('div', class_='stockcodec').find('div', id='zw_body').text
            result = u""
            result = result + article
    except Exception, e:
        article = soup.find('div', class_='stockcodec').text
        result = article.replace("\n","").replace("\r","").replace(" ","")
    publish_date = soup.find('div', class_='zwfbtime').contents[-1].string
    temp = re.findall('\d+', publish_date, re.S)
    publish_date = temp[0] + "-" + temp[1] + "-" + temp[2]
    publish_date = publish_date.encode("ascii")
    return result,publish_date

def get_content2(url):
    headers = {
        'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.79 Safari/537.36 Edge/14.14393",
        # 'Accept': "application/json, text/javascript, */*; q=0.01",
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
    soup = BeautifulSoup(content, "lxml")
    # print soup
    # article = soup.find('div',class_ = 'stockcodec').find('p', style="line-height: 164.28%;").contents
    article = soup.find('div', class_='stockcodec').contents
    result = u""

    result = result + article[5].string
    for i in range(6, len(article) - 1):
        items = article[i].contents[0]
        if items != None:
            result = result + items.string

    # for each in article[3].contents:
    #     items = each.string
    #     if items != None:
    #         result = result + items
    comment = soup.findAll('div', class_='zwlitext stockcodec')
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

    return result, commentres, publish_date
# get_content(url)

def get_pageinfo(url):
    data = get_infoJson(url)
    soup = BeautifulSoup(data, "lxml")
    result = []
    b = soup.findAll('div', class_='articleh')
    for each in b:
        #print each.contents

        item = {}
        try:
            t = each.contents
            item["readcount"] = t[1].text
            item["commentcount"] = t[2].text
            url = "http://guba.eastmoney.com"
            # url = url + t[3].contents[-1].attrs['href']
            # temp = t[3].contents[-1]
            temp = str(t[3])
            #print re.findall(r'<span class="l3">(.*?)</a></span>',temp,re.S)
            part_url = re.findall(r'<a href="(.*?)"', temp, re.S)[0]
            if part_url[0] == "/":
                url = url + part_url
            else:
                url = url + '/' + part_url
            tit = re.findall(r'title=(.*?)>', temp, re.S)[0]
            item["url"] = url
            item["title"] = re.findall(r'title="(.*?)">', temp, re.S)[0]
            # item["publish_date"] = get_date(str(t[5].text))
            # url = "http://guba.eastmoney.com/news,600060,105041596.html"
            content,publish_date = get_content1(url)
            item["content"] = content
            # item["comment"] = comment
            item["publish_date"] = publish_date
            sleeptime = random.random() + 0.1
            time.sleep(sleeptime)
            result.append(item)
        except Exception, e:
            print Exception, " page_info:", e
    return result

# 将数据插入到数据库中
def deal_sql(url,stockid):
    conn = MySQLdb.connect(
        host='192.168.2.197',
        port=3306,
        user='root',
        passwd='123',
        db='stock'
    )
    conn.set_character_set("utf8")
    cur = conn.cursor()
    info = get_pageinfo(url)
    n = len(info)
    flag = 1
    for i in range(n):
        temp = info[i]
        readcount = int(temp['readcount'].decode("utf-8"))
        commentcount = int(temp['commentcount'].decode("utf-8"))
        content = temp['content']
        # content = content
        title = temp['title']
        url = temp['url']
        # comment = temp['comment']
        publish_date = temp["publish_date"]
        # stockid = "600060"
        #print title
        # sleeptime = random.random() + 0.072
        # time.sleep(sleeptime)
        try:
            sql_main = "insert into notice(stockid,readcount,commentcount,publish_date,title,url,content) values " \
                       "(\"" + stockid + "\" ," + str(readcount) + " ," + str(commentcount) + " ,\"" + publish_date + "\" ,  \"" + title + \
                       "\" ,\"" + url + "\",\"" + content + "\");"
            print sql_main
            cur.execute(sql_main)
            conn.commit()
        except Exception, e:
            print Exception, ":", e
            flag = 0
    cur.close()
    conn.close()
    return flag

# 按页爬取
def get_Result(start,n,stockid):
    urls = get_pageUrl(start,n,stockid)
    page_num = 1
    for i in range(page_num):
        try:
            flag = deal_sql(urls[i],stockid)
            if flag == 0:
                break
            else:
                sleeptime = random.random() + 0.001
                time.sleep(sleeptime)
                page_num = page_num + 1
        except Exception,e:
            print Exception, ":", e


# begin = datetime.datetime.now()
# n = 7
# # 爬取到多少页
# start = 1
# stockid = "002020"
# #stockids = [ ,"000927","002362",
# # "600000","600060","600887","601318","601939","601857","601988","601398","600594","002230","000063","000651","600115","000538","600085","000568","000333","000895","600054","000858"]
# get_Result(start,n,stockid)
# end = datetime.datetime.now()
# print begin,end,end - begin

stockid_list = ["603778","600634","600962","600562","600213"]
for stockid in stockid_list:
    begin = datetime.datetime.now()
    n = 1
    # 爬取到多少页
    start = 1
    #stockids = [ ""002447","300362","601700","600249","002297","603058","300226","002807","000638","002836","000563","000816","002382","002826","300431","002700","300561","300109","603676","000718","002576","601636","002826","300542","300236","002382","600760","002015","002883","300675","002020" ,"002362",
    # "600887","601318","601939","601857","601988","601398","600594","002230","000063","000651","600115","000538","600085","000568","000333","000895","600054","000858"]
    get_Result(start,n,stockid)
    end = datetime.datetime.now()
    print begin,end,end - begin