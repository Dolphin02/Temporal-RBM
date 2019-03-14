# -*- coding: utf-8 -*-
import codecs
import os
import MySQLdb

def listdir(path,list_name):
    for file in os.listdir(path):
        file_path = os.path.join(path,file)
        if os.path.isdir(file_path):
            listdir(file_path,list_name)
        elif os.path.splitext(file_path)[1] == ".csv":
            # list_name.append(file_path[-10:])
            list_name.append(file_path)

def insret_data(stock_path):
    list_name = []
    listdir(stock_path, list_name)
    for each in list_name:
    # for each in ["C:\Users\Dolphin\Desktop\stockdeal\\399001.csv ","C:\Users\Dolphin\Desktop\stockdeal\\000001.csv "]:
        file = codecs.open(each, 'r', 'gbk')
        stockid = each[-10:-4]
        header = file.readline()
        line = file.readline()
        res = []

        conn = MySQLdb.connect(
            host='192.168.2.197',
            port=3306,
            user='root',
            passwd='123',
            db='stock',
        )
        conn.set_character_set("utf8")
        cur = conn.cursor()

        while line:
            item = []
            l = line.encode('utf-8')
            all = l.split(',')
            for each in all:
                date = all[0].replace('/', '-')
                close = float(all[3])
                high = float(all[4])
                low = float(all[5])
                openprice = float(all[6])

                if close == 0.0 or all[8] == None:
                    continue
                elif close == high == low == openprice:
                    continue
                try:
                    pre_close = float(all[7])
                    amount_change = float(all[8])
                    quote_change = float(all[9])
                    volume = float(all[11])
                except Exception, e:
                    print Exception, ":", e
                item.append(each)
            # print item
            # if stockid[0] == "0" or stockid[0] == "3":
            #     stock_label = "shen"
            # elif stockid[0] == "6":
            #     stock_label = "shang"
            stock_label = "price"
            sql_main = "insert into " + stock_label + " (stockid,stocktype,date,open,high,low,close,pre_close,amount_change,quote_change,volume) values " \
                                                      "(\"" + str(stockid) + "\" ," + str(1) + " ,\"" + date + "\" ,  " + str(openprice) + \
                       " ," + str(high) + "," + str(low) + "," + str(close) + "," + str(pre_close) + "," + str(amount_change) + "," + str(quote_change) + "," + str(volume) + ");"
            print sql_main
            cur.execute(sql_main)
            conn.commit()
            res.append(item)
            line = file.readline()

# stock_path = "C:\Users\Dolphin\Desktop\stockdeal"
# insret_data(stock_path)




