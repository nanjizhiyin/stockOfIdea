#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author:洪卫

import tkinter as tk  # 使用Tkinter前需要先导入
import tushare as ts
import stockOne
import mail
import csv
from apscheduler.schedulers.blocking import BlockingScheduler


# 第1步，实例化object，建立窗口window
window = tk.Tk()

# 第2步，给窗口的可视化起名字
window.title('股市实时分析')

# 第3步，设定窗口的大小(长 * 宽)
window.geometry('500x300')  # 这里的乘是小x


# 第4步，在图形界面上设定标签
var = tk.StringVar()    # 将label标签的内容设置为字符类型，用var来接收hit_me函数的传出内容用以显示在标签上
l = tk.Label(window, textvariable=var, bg='green', fg='white', font=('Arial', 12), width=30, height=2)
# 说明： bg为背景，fg为字体颜色，font为字体，width为长，height为高，这里的长和高是字符的长和高，比如height=2,就是标签有2个字符这么高
l.pack()


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
        mail.sendMail('可以买了',mailText)
    else:
        print("没有可买的")

# 定义一个函数功能（内容自己自由编写），供点击Button按键时调用，调用命令参数command=函数名
on_hit = False
# BlockingScheduler
scheduler = BlockingScheduler()
def hit_me():
    global on_hit
    global scheduler
    if on_hit == False:
        on_hit = True
        var.set('分析中,结果会发送到邮箱')

        scheduler.add_job(stockList, 'cron', day_of_week='1-5', hour='9-15', minute='*/5')
        scheduler.start()
    else:
        on_hit = False
        var.set('')
        #scheduler.shutdown()
        scheduler.shutdown(wait=False)

# 第5步，在窗口界面设置放置Button按键
button = tk.Button(window, text='开始分析', font=('Arial', 12), width=10, height=1, command=hit_me)
button.pack()


# 第6步，主窗口循环显示
window.mainloop()
# 注意，loop因为是循环的意思，window.mainloop就会让window不断的刷新，如果没有mainloop,就是一个静态的window,传入进去的值就不会有循环，mainloop就相当于一个很大的while循环，有个while，每点击一次就会更新一次，所以我们必须要有循环
# 所有的窗口文件都必须有类似的mainloop函数，mainloop是窗口文件的关键的关键。