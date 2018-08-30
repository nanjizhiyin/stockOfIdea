#!/usr/bin/python
# coding: UTF-8

import tushare as ts
import numpy as np
import pandas as pd
import talib
import stockstats
import stockMacd

def analysisStock( stockCode, stockName ):

    df = ts.get_k_data('300648')
    if  df.empty:
        return
    stockStat = stockstats.StockDataFrame.retype(df)
    # MACD
    difList = stockStat.get('macd')
    deaList = stockStat.get('macds')

    # 计算macd
    dif1 = 0
    dea1 = 0
    dif2 = 0
    dea2 = 0
    difList = difList.tail(2)
    deaList = deaList.tail(2)
    forIndex = 0
    for index in difList.index:
        if forIndex == 0:
            dif2 = difList[index]
            dea2 = deaList[index]
        elif forIndex == 1:
            dif1 = difList[index]
            dea1 = deaList[index]

        forIndex += 1

    # 如果macd在负数.与前一天相比增大了,买入信号
    # print("macd1="+str(macd1)+"\nmacd2="+str(macd2))

    # 买入等级
    buyLevel = 0

    # MACD将要发生金叉
    if dif1 < 0 and dif1 - dea1 > dif2 - dea2:
        buyLevel += 1
    else:
        return

    # 计算KDJ
    kdjk = stockStat['kdjk']
    kdjd = stockStat['kdjd']
    # kdjj = stockStat['kdjj']


    k1 = 0
    d1 = 0
    k2 = 0
    d2 = 0
    kdjk = kdjk.tail(2)
    kdjd = kdjd.tail(2)
    forIndex = 0
    for index in kdjk.index:
        if forIndex == 0:
            k2 = kdjk[index]
            d2 = kdjd[index]
        elif forIndex == 1:
            k1 = kdjk[index]
            d1 = kdjd[index]

        forIndex += 1

    # KD与前一天相比差值变小了

    # 计算差值
    c1 = k1 - d1
    c2 = k2 - d2

    # kd差值在减小,将要金叉
    if d1 > k1 and c1 < c2:
        buyLevel += 1
    else:
        return

    # 邮件内容
    mailText = stockCode + '--' + stockName
    mailText += "--MACD指标满足"
    mailText += "--KDJ指标满足"

    if buyLevel == 2 :
        print(mailText)
        return mailText


