# -*-coding:utf-8 -*-
import MySQLdb
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import rcParams
import seaborn as sns
import numpy as np
from numpy.random import randn
import matplotlib as mpl
import matplotlib.pyplot as plt
from scipy import stats
import deal_stock
# 统计涨跌幅的范围
def count_quoteChange(dataset,stockid,start,end):
    conn = MySQLdb.connect(
        host='192.168.2.197',
        port=3306,
        user='root',
        passwd='123',
        db='stock',
    )
    conn.set_character_set("utf8")
    cur = conn.cursor()

    sql_select = 'select * from %s where stockid = %s and date between "%s" and "%s" order by date desc;' % (dataset,stockid,start,end)
    aa = cur.execute(sql_select)
    info = cur.fetchmany(aa)
    conn.commit()

    data = []
    for each in info:
        if each[4] != 0.0:
            data.append(each[10])
    return data






def show_statistics(data,stockid):
    # fig1 = plt.figure(2)
    # rects = plt.bar(left = (0.2,1),height = (1,0.5),width = 0.2,align="center",yerr=0.000001)
    plt.title("count")
    plt.hist(data, bins=12, color=sns.desaturate("indianred", .8), alpha=.4)
    plt.savefig('C:\Users\Dolphin\Desktop\statistics\ ' + stockid + '.jpg')
    plt.show()


def get_stockid(path):
    list_name = []
    stockids = []
    deal_stock.listdir(path, list_name)
    for each in list_name:
        stockids.append(each[-10:-4])
    return stockids

# dataset = "price"
# start = "2010-01-01"
# end = "2017-09-30"
# stock_path = "C:\Users\Dolphin\Desktop\stockdeal"
# stockids = get_stockid(stock_path)
#
# for stockid in stockids:
#     change = count_quoteChange(dataset,stockid,start,end)
#     show_statistics(change,stockid)

