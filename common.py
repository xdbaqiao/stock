#!/usr/bin/env python2
# coding: utf-8

import re
import json
from download import download 

def get_latest_information(stock_code):
    fields = ['股票名称', '今日开盘价', '昨日收盘价', '当前价格', '今日最高价',\
            '今日最低价', '竞买价', '竞卖价', '成交量', '成交额', '买一/股', '买一/元',\
             '买二/股', '买二/元', '买三/股', '买三/元', '买四/股', '买四/元', '买五/股',\
             '买五/元', '卖一/股', '卖一/元','卖二/股', '卖二/元', '卖三/股', '卖三/元',\
             '卖四/股', '卖四/元', '卖五/股', '卖五/元', '日期', '时间']
    sina_api = 'http://hq.sinajs.cn/list=%s' % stock_code
    html = download(sina_api).get(sina_api)
    if not html:
        return ()
    html = html.decode('gbk')
    bag = {}
    for inum, i in enumerate(html.split(",")):
        bag[fields[inum]] = i
    return json.dumps(bag)



if __name__ == '__main__':
    stock_code = 'sh601006'
    print get_latest_information(stock_code)
