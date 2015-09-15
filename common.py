#!/usr/bin/env python2
# coding: utf-8

import re
import json
from download import download 

def get_latest_information(stock_code):
    # get the latest stock information
    # return json format result
    fields = [u'股票名称', u'今日开盘价', u'昨日收盘价', u'当前价格', u'今日最高价',\
            u'今日最低价', u'竞买价', u'竞卖价', u'成交量', u'成交额', u'买一/股', u'买一/元',\
             u'买二/股', u'买二/元', u'买三/股', u'买三/元', u'买四/股', u'买四/元', u'买五/股',\
             u'买五/元', u'卖一/股', u'卖一/元',u'卖二/股', u'卖二/元', u'卖三/股', u'卖三/元',\
             u'卖四/股', u'卖四/元', u'卖五/股', u'卖五/元', u'日期', u'时间', u'code']
    sina_api = 'http://hq.sinajs.cn/list=%s' % stock_code
    html = download(sina_api).get(sina_api)
    html = html.decode('gbk').strip()
    bag = {}
    try:
        m = re.compile(r'"([^"]+)"').search(html)
        info = m.groups()[0] if m else ''
        for inum, i in enumerate(info.split(",")):
            bag[fields[inum]] = i
    except IndexError:
        print 'IndexError...'
    return json.dumps(bag, sort_keys=True, ensure_ascii=False).encode('utf8')

def get_history_volume(start_date='20130915', end_date='20150915'):
    # 上证指数历史成交量
    url = 'http://q.stock.sohu.com/hisHq?code=zs_000001&start=%s&end=%s&stat=1&order=D&period=d&callback=historySearchHandler&rt=jsonp' % (start_date, end_date)
    html = download(url).get(url)
    html = html.decode('gbk')
    m = re.compile(r'Handler\(\[(.*)\]\)', flags=re.IGNORECASE).search(html.strip())
    json_data = m.groups()[0] if m else ''
    bag = {}
    try:
        datas = json.loads(json_data)
        for i in datas['hq']:
            bag[i[0].replace('-', '')] = i[-3]
    except Exception:
        print 'json data null...'
    return bag

if __name__ == '__main__':
    #stock_code = 'sh601006'
    #print get_latest_information(stock_code)
    from gnuplot import gnuplot
    bag = get_history_volume()
    gnuplot(x=len(bag.keys()), y=bag.values(), title='上证指数历史成交量')

