#!/usr/bin/python
# coding: UTF-8

import tushare as ts
import stockstats

def analysisStock( stockCode, stockName ):

    df = ts.get_k_data(stockCode)
    if  df.empty:
        return

    # 买入等级
    buyLevel = 0

    # 邮件内容
    mailText = stockCode + '--' + stockName

    stockStat = stockstats.StockDataFrame.retype(df)
    # MACD
    # 计算macd

    macdList = stockStat.get('macdh')
    macdList = macdList.tail(2)
    macd1 = 0
    macd2 = 0
    forIndex = 0
    for index in macdList.index:
        if forIndex == 0:
            macd2 = macdList[index]
        elif forIndex == 1:
            macd1 = macdList[index]
        forIndex += 1
    if macd1 < 0 and macd1 < macd2:
        buyLevel += 1
        mailText += "--MACD下行"

    # 计算dif,dea
    # 当天和前天的数据
    # difList = stockStat.get('macd')
    # deaList = stockStat.get('macds')
    # difList = difList.tail(2)
    # deaList = deaList.tail(2)
    # dif1 = 0
    # dif2 = 0
    # dea1 = 0
    # dea2 = 0
    # forIndex = 0
    # for index in difList.index:
    #     if forIndex == 0:
    #         dif2 = difList[index]
    #         dea2 = deaList[index]
    #     elif forIndex == 1:
    #         dif1 = difList[index]
    #         dea1 = deaList[index]
    #
    #     forIndex += 1
    #
    # # 如果macd在负数.与前一天相比增大了,买入信号
    # c1 = dea1 - dif1
    # c2 = dea2 - dif2
    # # MACD将要发生金叉
    # if dif1 < 0 and c1 < c2:
    #     buyLevel += 1
    #     mailText += "--MACD将金叉"

    # 计算KDJ
    kdjk = stockStat['kdjk']
    kdjd = stockStat['kdjd']
    kdjj = stockStat['kdjj']

    # 当天和昨天的数据
    kdjk = kdjk.tail(2)
    kdjd = kdjd.tail(2)
    kdjj = kdjj.tail(2)

    k1 = 0
    d1 = 0
    j1 = 0
    # k2 = 0
    # d2 = 0
    j2 = 0
    forIndex = 0
    for index in kdjj.index:
        if forIndex == 0:
            # k2 = kdjk[index]
            # d2 = kdjd[index]
            j2 = kdjj[index]
        elif forIndex == 1:
            k1 = kdjk[index]
            d1 = kdjd[index]
            j1 = kdjj[index]

        forIndex += 1

    # kd差值在减小,将要金叉
    if d1 > k1 and k1 > j1 and j1 > j2:
        buyLevel += 1
        mailText += "--KDJ将金叉"



    if buyLevel == 2 :
        print(mailText)
        return mailText


