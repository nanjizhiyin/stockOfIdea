#!/usr/bin/python
# coding: UTF-8
# http://tushare.org/fundamental.html#id2
# 业绩报告（主表）
# 按年度、季度获取业绩报表数据。数据获取需要一定的时间，网速取决于您的网速，请耐心等待。结果返回的数据属性说明如下：

import tushare as ts
import time

def report_data():

    #获取2014年第3季度的业绩报表数据
    #季度 :1、2、3、4，只能输入这4个季度
    quarter = 1
    # 获取当前的年和月
    nowYear = int(time.strftime('%Y',time.localtime(time.time())))
    nowMonth = int(time.strftime('%m',time.localtime(time.time())))
    if nowMonth <= 3:
        # 上一年的第四季度
        nowYear -= 1
        quarter = 4

    elif nowMonth <= 6:
        # 第一季度
        quarter = 1

    elif nowMonth <= 9:
        # 第一季度
        quarter = 2

    elif nowMonth <= 12:
        # 第一季度
        quarter = 3

    rd = ts.get_report_data(nowYear,quarter)
    rd.to_csv('report_data.csv')


if __name__ == '__main__':
    report_data()
