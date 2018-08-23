#!/usr/bin/python
# coding: UTF-8

import tushare as ts
import numpy as np
import talib

df = ts.get_k_data('300648', start='2018-07-20', end='2018-08-23')

# 输出一个字段
for index, row in df.iterrows():
    print(row['date'])

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

# MACD输出
index = 0
for item in macd:
    tmpMacd = macd[index]
    if not np.isnan(tmpMacd):
        print("\n日期:"+date[index]+"\n DIF ="+str(macd[index])+"\n DEA ="+str(signal[index])+" \n MACD="+str(hist[index]))
    index += 1

# 计算KDJ
k,d = talib.STOCH(df['high'].values,
                  df['low'].values,
                  df['close'].values,
                  fastk_period=9,
                  slowk_period=3,
                  slowk_matype=0,
                  slowd_period=3,
                  slowd_matype=0)

# KD输出
index = 0
for item in k:
    tmpValue = k[index]
    if not np.isnan(tmpValue):
        print("\n日期:"+date[index]+"\n K ="+str(k[index])+"\n D ="+str(d[index]))
    index += 1



