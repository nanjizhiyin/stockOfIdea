#!/usr/bin/python
# coding: UTF-8

import tushare as ts
import time
import oneStock
import mail


# returnStr = oneStock.analysisStock('603997','继峰股份')

# 获取当前的日期
nowTime = time.strftime('%Y-%m-%d',time.localtime(time.time()))

# 股票列表
df = ts.get_stock_basics()

#直接保存
# df.to_excel('d:/stock/'+nowTime+'.xlsx')

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
