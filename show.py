#!/usr/bin/python
# coding: UTF-8

"""This script parse stock info"""

import tushare as ts
import pymongo
import json

def get_all_price(code_list):
    '''process all stock'''
    df = ts.get_realtime_quotes(code_list)
    print(df)


    conn = pymongo.MongoClient('10.10.1.169', port=27017,tz_aware=False)
    db = conn.get_database("admin")
    db.authenticate("root", "5211314")
    db = conn.get_database("stock")
    db.tickdata.insert(json.loads(df.to_json(orient='records')))

if __name__ == '__main__':
    STOCK = ['300648',
             '601668']

    get_all_price(STOCK)
