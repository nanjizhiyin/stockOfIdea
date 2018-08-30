#!/usr/bin/python
# coding: UTF-8

import tushare as ts
import oneStock
import mail

def stockList():
    # 股票列表
    df = ts.get_stock_basics()

    # 邮件内容
    mailText = ""
    # 输出一个字段
    for index, row in df.iterrows():
        print(index +"--"+ row['name'])
        returnStr = oneStock.analysisStock(index,row['name'])
        if returnStr != None:
            mailText += returnStr+'\n'


    if mailText != "" :
        mail.sendMail(mailText)
    else:
        mail.sendMail("没有可买的股票")

if __name__ == '__main__':
    # stockList()
    returnStr = oneStock.analysisStock('300648','test')
    print(returnStr)
