#!/usr/bin/python
# coding: UTF-8

import tushare as ts
import numpy as np
import talib
import time
import smtplib
from email.mime.text import MIMEText
from email.header import Header

def sendMail( text ):
    # 第三方 SMTP 服务
    mail_host="smtp.163.com"  #设置服务器
    mail_user="nanjizhiyin@163.com"    #用户名
    mail_pass="wu5211314"   #口令
    sender = 'nanjizhiyin@163.com'
    receivers = ['gaojindan@163.com']  # 接收邮件，可设置为你的QQ邮箱或者其他邮箱

    # 三个参数：第一个为文本内容，第二个 plain 设置文本格式，第三个 utf-8 设置编码
    message = MIMEText(text, 'plain', 'utf-8')
    message['From'] = sender   # 发送者
    message['To'] =  ";".join(receivers)        # 接收者

    subject = '可以买了'
    message['Subject'] = Header(subject, 'utf-8')

    try:
        smtpObj = smtplib.SMTP()
        smtpObj.connect(mail_host, 25)    # 25 为 SMTP 端口号
        smtpObj.login(mail_user,mail_pass)
        smtpObj.sendmail(sender, receivers, message.as_string())
        print ("邮件发送成功")
    except smtplib.SMTPException:
        print ("Error: 无法发送邮件")

# 获取N天前的时间
dayNum = 31
for20Time = time.strftime('%Y-%m-%d',time.localtime(time.time()-dayNum*24*60*60))
nowTime = time.strftime('%Y-%m-%d',time.localtime(time.time()))
df = ts.get_k_data('300648', start=for20Time, end=nowTime)

# 输出一个字段
# for index, row in df.iterrows():
#     print(row['date'])

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
# index = 0
# for item in macd:
#     tmpMacd = macd[index]
#     if not np.isnan(tmpMacd):
#         print("\n日期:"+date[index]+"\n DIF ="+str(macd[index])+"\n DEA ="+str(signal[index])+" \n MACD="+str(hist[index]))
#     index += 1

# 如果macd在负数.与前一天相比增大了,买入信号
macdNum = macd.size
macd1 = macd[macdNum-1]
macd2 = macd[macdNum-2]

# 邮件内容
mailText = None
# 买入信号
if  macd1 < 0 and macd1 > macd2:
    mailText += "MACD指标满足"


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
# index = 0
# for item in k:
#     tmpValue = k[index]
#     if not np.isnan(tmpValue):
#         print("\n日期:"+date[index]+"\n K ="+str(k[index])+"\n D ="+str(d[index]))
#     index += 1

# 如果KD在负数.与前一天相比差值变小了
kdjNum = k.size
k1 = k[kdjNum-1]
k2 = k[kdjNum-2]

d1 = d[kdjNum-1]
d2 = d[kdjNum-2]

if mailText != None :
    sendMail(mailText)



