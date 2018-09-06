#!/usr/bin/python
# coding: UTF-8

import tushare as ts
import stockOne
import mail

def stockList():
    # 股票列表
    df = ts.get_stock_basics()
    # 市盈率
    kPe = 50
    # 邮件内容
    mailText = ""
    # 计算个数
    mNumber = 0
    # 输出一个字段
    for index, row in df.iterrows():
        print(index +"--"+ row['name'])
        # 市盈率
        pe = row['pe']
        if pe > kPe:
            print('市盈率大于'+str(kPe))
            continue
        name = row['name']
        if name.find('ST') > -1:
            print("抛弃st")
            continue

        returnStr = stockOne.analysisStock(index, name)
        if returnStr != None:
            mailText += returnStr+'\n'
            mNumber += 1


    if mailText != "" :
        print("找到"+str(mNumber)+"个")
        mail.sendMail(mailText)
    else:
        mail.sendMail("没有可买的")

if __name__ == '__main__':
    stockList()
    # returnStr = oneStock.analysisStock('300648','test')
    # print(returnStr)
