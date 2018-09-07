#!/usr/bin/python
# coding: UTF-8

import tushare as ts
import stockOne
import mail
import csv

def stockList():

    # 盈利的code
    profitList = []
    csv_reader = csv.reader(open("report_data.csv",'r', encoding='UTF-8'))
    index = 0
    for row in csv_reader:
        if index == 0:
            index = 1
            continue

        code = row[1]
        # print(code)

        # 每股收益
        eps = row[3]
        if eps:
            eps = float(eps)
        else:
            eps = 0

        # 每股收益同比(%)
        eps_yoy = row[4]
        if eps_yoy:
            eps_yoy = float(eps_yoy)
        else:
            eps_yoy = 0

        # 净资产收益率
        roe = row[6]
        if roe:
           roe = float(roe)
        else:
            roe = 0

        # 净利率
        net_profits = row[8]
        if net_profits:
            net_profits = float(net_profits)
        else:
            net_profits = 0

        # 净利润同比(%)
        profits_yoy = row[9]
        if profits_yoy:
            profits_yoy = float(profits_yoy)
        else:
            profits_yoy = 0

        if eps > 0 and eps_yoy > 0 and roe > 0 and net_profits > 0 and profits_yoy > 0:
            profitList.append(code)

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
        if index not in profitList:
            print('上一季度没有盈利')
            continue
        # 市盈率
        pe = row['pe']
        if pe > kPe:
            print('市盈率大于'+str(kPe))
            continue

        # 每股收益
        esp = row['esp']
        if esp < 0:
            print("每股收益为负")
            continue

        # 市净率
        pb = row['pb']
        if pb > 3:
            print("市净率大于3了")
            continue

        # 收入同比(%)
        rev = row['rev']
        if rev < 0:
            print("收入同比为负")
            continue
        # 利润同比(%)
        profit = row['profit']
        if profit < 0:
            print("利润同比为负")
            continue
        # 毛利率(%)
        gpr = row['gpr']
        if gpr < 0:
            print("毛利率为负")
            continue
        # 净利润率(%)
        npr = row['npr']
        if npr < 0:
            print("净利润率为负")
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
    # returnStr = stockOne.analysisStock('300648','test')
    # print(returnStr)
