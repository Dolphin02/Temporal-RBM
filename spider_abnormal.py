# -*-coding:utf-8 -*-
import codecs
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
import statistics
import deal_stock
reload(sys)
sys.setdefaultencoding('utf8')

def get_date(dateTime):

    result = ""
    if int(dateTime[1]) < 5:
        result = "2017-" + dateTime
    else:
        result = "2016-" + dateTime
    return result

# 获取机构研报的所有内容
def get_info(url):
    headers = {
    'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36",
    'Cookie': "emstat_bc_emcount=34332052573139921851; st_pvi=38217938751377; st_si=30253519184358; emstat_ss_emcount=9_1491851647_1806674426"}
    html = requests.get(url, headers=headers).content
    soup = BeautifulSoup(html, "lxml")
    all_date = soup.find('div', class_='content-box').contents[9].contents[1].text
    date = all_date.split("\n")
    res_date = []
    for each in date:
        if len(each) > 0:
            temp = each.replace(u"年","-").replace(u"月","-").replace(u"日","-")
            if len(temp[:-5]) > 5:
                res_date.append(temp[:-5])
    return res_date

def gen_urls(stockids):
    part_url = "http://data.eastmoney.com/stock/lhb/"
    urls = []
    for stockid in stockids:
        urls.append(part_url + stockid + ".html")
    return urls


def get_dataTab(date, stockid):
    url = "http://data.eastmoney.com/stock/lhb," + date + "," + stockid + ".html"
    headers = {
        'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36",
        'Cookie': "emstat_bc_emcount=34332052573139921851; st_pvi=38217938751377; st_si=30253519184358; emstat_ss_emcount=9_1491851647_1806674426"}
    try:
        html = requests.get(url, headers=headers).content
        soup = BeautifulSoup(html, "lxml")
        all_info = soup.find('div', class_='data-tips').contents
        res = all_info[1].text[19:]
        return res
    except Exception,e:
        print stockid


def get_date():
    begin = datetime.datetime.now()
    stock_path = "C:\Users\Dolphin\Desktop\stockdeal"
    # stockids = statistics.get_stockid(stock_path)
    # stockids = ["603778","600634","601700","600249","002297","603058","300226","002807","000638","002836","000563","000816","002382","002826","300431","002700","300561","300109","603676","000718","002576","601636","002826","300542","300236","002382","600760","002015","002883","300675","002447","300362","002020","002655","002188","000591","300612""002863","603689","002902","600161","601069","002895","300465", "300612","300468","002068","600520","300710","600137","300019","300431","300034","002053","603222","300708","002505","300249","300229","002801","200168","300384", "002194","300176","000789","002839","002422","002895","000671","300672","300666","002594","002675","000005","002619","600386","002853","300639","002507","000927",300698",300026", "600617","000836","603160","002336", "600609", "000623", "600212", "000813", "600380", "000623", "300088","002739", "002199","002730","300267","600238","002254","002651","002281","300316","603577","603559","603938", "600559", "600000","600060","600887","601318","601939","601857","601988","601398","600594","002230","000063","000651","600115","000538","600085","000568","000333","000895","600054","000858", "600331","300678","600805"]
    stockids = ["600962","600562","600213"]


    urls = gen_urls(stockids)
    file_write = codecs.open("C://Users//Dolphin//Desktop//stockdate//volatitily_sample.txt ", "a", "utf-8")
    for url in urls:
        date = get_info(url)
        stockid = url[-11:-5]
        for each_date in date:
            type = get_dataTab(each_date,stockid)
            item = stockid + " " + each_date + " " + type
            file_write.write(item)
            file_write.write("\n")
            sleeptime = 0.5*random.random()
            time.sleep(sleeptime)
            print item
    end = datetime.datetime.now()
    print begin, end, end - begin

get_date()
