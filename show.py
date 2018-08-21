#!/usr/bin/python
# coding: UTF-8

import tushare as ts
import matplotlib.pyplot as plt
import numpy as np
import talib

df=ts.get_k_data('300648', start='2018-07-01', end='2018-08-21')
close = [float(x) for x in df['close']]
# 调用talib计算指数移动平均线的值
df['EMA12'] = talib.EMA(np.array(close), timeperiod=6)
df['EMA26'] = talib.EMA(np.array(close), timeperiod=12)

# 调用talib计算MACD指标
macd,signal,hist = talib.MACD(np.array(close),
                                      fastperiod=6,
                                      slowperiod=12,
                                      signalperiod=9)


index = 0
for item in macd:
    tmpMacd = macd[index]
    if not np.isnan(tmpMacd):
        print("\n DIF ="+str(macd[index])+"\n DEA ="+str(signal[index])+" \n MACD="+str(hist[index]))
    index += 1
