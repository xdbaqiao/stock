#!/usr/bin/env python2
# coding: utf-8
# http://www.cninfo.com.cn/cninfo-new/announcement/query

import re
import json
import  time
from common import common_re, UnicodeWriter
from download import download

FIELDS = ['关键字', '代码', '简称', '公告标题', '公告时间', 'PDF文件URL']

def read_conf():
    return [i.strip() for i in open('setting.info')]

def get_last_trade_date():
    url = 'http://data.eastmoney.com/stock/lhb.html'
    html = download().get(url)
    m = common_re(r'"readonly"\svalue\="([^"]+)"', html)
    if m:
        return m
    else:
        print 'Error: Can not get last trade date!'
        return ''

def scrape(sdate):
    writer = UnicodeWriter('cninfo.csv')
    writer.writerow(FIELDS)
    D = download('http://www.cninfo.com.cn/cninfo-new/announcement/show', is_cookie=True)
    url = 'http://www.cninfo.com.cn/cninfo-new/announcement/query'
    last_date = get_last_trade_date()
    for k in read_conf():
        post_data = {}
        post_data['searchkey'] = k
        post_data['column'] = 'szse'
        post_data['columnTitle'] = '历史公告查询'
        post_data['pageNum'] =  '1'
        post_data['pageSize'] = '30'
        post_data['tabName'] = 'fulltext'
        if sdate:
            post_data['seDate'] = sdate
        else:
            post_data['seDate'] = last_date if last_date else '请选择日期'
        html = D.post(url, data = post_data)
        jdata = json.loads(html).get('announcements')
        if jdata:
            for i in jdata:
                bag = {}
                bag['关键字'] = k
                bag['代码'] = str(i.get('secCode'))
                bag['简称'] = i.get('secName')
                bag['公告标题'] =  i.get('announcementTitle')
                stime = str(i.get('announcementTime'))
                x = time.localtime(float(stime[:-3])) if stime else ''
                bag['公告时间'] = time.strftime('%Y-%m-%d', x)
                m = i.get('announcementId')
                bag['PDF文件URL'] = 'http://www.cninfo.com.cn/cninfo-new/disclosure/szse/bulletin_detail/true/' + m if m else ''
                writer.writerow(bag.get(field) for field in FIELDS)

if __name__ == '__main__':
    sdate = raw_input('请输入统计开始日期，如20141109：')
    edate = raw_input('请输入统计结束日期，如20151109：')
    idate = '%s ~ %s'% ('-'.join([sdate[:4], sdate[4:6], sdate[6:]]), '-'.join([edate[:4], edate[4:6], edate[6:]]))
    scrape(idate)
