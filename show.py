#!/usr/bin/python
# coding: UTF-8

"""This script parse stock info"""

import tushare as ts

def get_all_price(code_list):
    '''process all stock'''
    df = ts.get_realtime_quotes(code_list)
    print(df)

if __name__ == '__main__':
    STOCK = ['300648',
             '601668']

    get_all_price(STOCK)
