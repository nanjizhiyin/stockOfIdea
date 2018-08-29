#!/usr/bin/python
# coding: UTF-8

import tushare as ts
import numpy as np
import talib
import time
import mail


# 获取N天前的时间
dayNum = 31
for20Time = time.strftime('%Y-%m-%d',time.localtime(time.time()-dayNum*24*60*60))
# 获取当前的日期
nowTime = time.strftime('%Y-%m-%d',time.localtime(time.time()))
# 获取一只股票的数据
df = ts.get_k_data('300648', start=for20Time, end=nowTime)

date = [str(x) for x in df['date']]
close = [float(x) for x in df['close']]

# 调用talib计算指数移动平均线的值
df['EMA12'] = talib.EMA(np.array(close), timeperiod=6)
df['EMA26'] = talib.EMA(np.array(close), timeperiod=12)

# 调用talib计算MACD指标
macd,signal,hist = talib.MACD(np.array(close),
                                      fastperiod=6,
                                      slowperiod=12,
                                      signalperiod=9)


# 如果macd在负数.与前一天相比增大了,买入信号
macdNum = macd.size
macd1 = macd[macdNum-1]
macd2 = macd[macdNum-2]

# 邮件内容
mailText = ""
# 买入等级
# 买入信号
buyLevel = 0
if macd1 < 0 and macd1 > macd2:
    mailText += "MACD指标满足\n"
    buyLevel += 1


# 计算KDJ
k,d = talib.STOCH(df['high'].values,
                  df['low'].values,
                  df['close'].values,
                  fastk_period=9,
                  slowk_period=3,
                  slowk_matype=0,
                  slowd_period=3,
                  slowd_matype=0)


# KD与前一天相比差值变小了
kdjNum = k.size
k1 = k[kdjNum-1]
k2 = k[kdjNum-2]

d1 = d[kdjNum-1]
d2 = d[kdjNum-2]


if k1 - d1 < k2 - d2:
    buyLevel += 1
    mailText += "KDJ指标满足\n"

if buyLevel == 2 :
    mail.sendMail(mailText)



