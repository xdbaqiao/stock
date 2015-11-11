#!/usr/bin/env python2
# coding: utf-8
# http://www.cninfo.com.cn/cninfo-new/announcement/query

import re
import json
import  time
import ConfigParser
from common import common_re, UnicodeWriter
from download import download

FIELDS = [u'关键字', u'代码', u'简称', u'公告标题', u'公告时间', u'PDF文件URL']

def read_conf():
    """Load settings
    """
    cfg = ConfigParser.ConfigParser()
    cfg.read('setting.ini')

    try:
        sdate= cfg.get('setting', 'start_date')
    except (ConfigParser.NoSectionError, ConfigParser.NoOptionError), e:
        sdate= ''
    try:
        edate= cfg.get('setting', 'end_date')
    except (ConfigParser.NoSectionError, ConfigParser.NoOptionError), e:
        edate = '' 

    idate = '%s ~ %s'% ('-'.join([sdate[:4], sdate[4:6], sdate[6:]]), '-'.join([edate[:4], edate[4:6], edate[6:]])) \
            if sdate and edate else ''
    try:
        szse_task= cfg.get('setting', 'szse_task')
        szse_tasks = szse_task.split(';') if  szse_task else []
        bond_task= cfg.get('setting', 'bond_task')
        bond_tasks = bond_task.split(';') if  bond_task else []
    except (ConfigParser.NoSectionError, ConfigParser.NoOptionError), e:
        raise Exception('Error: no task!')
    return [idate, szse_tasks, bond_tasks]

def get_last_trade_date():
    url = 'http://data.eastmoney.com/stock/lhb.html'
    html = download().get(url)
    m = common_re(r'"readonly"\svalue\="([^"]+)"', html)
    if m:
        return m
    else:
        print 'Error: Can not get last trade date!'
        return ''

def scrape():
    [sdate, szse_tasks, bond_tasks] = read_conf()
    writer = UnicodeWriter('cninfo.csv', 'gbk')
    writer.writerow(FIELDS)
    D = download('http://www.cninfo.com.cn/cninfo-new/announcement/show', is_cookie=True)
    url = 'http://www.cninfo.com.cn/cninfo-new/announcement/query'
    last_date = get_last_trade_date() if not sdate else ''
    post_data = {}
    post_data['columnTitle'] = '历史公告查询'
    post_data['pageNum'] =  '1'
    post_data['pageSize'] = '30'
    post_data['tabName'] = 'fulltext'
    if sdate:
        post_data['seDate'] = sdate
        print 'Query interval time is: %s' % sdate
    else:
        post_data['seDate'] = last_date if last_date else '请选择日期'
        print 'Last trade date is: %s' % last_date
    for k in szse_tasks + bond_tasks:
        post_data['column'] = 'szse' if k in szse_tasks else 'bond'
        post_data['searchkey'] = k
        try:
            html = D.post(url, data = post_data)
        except Exception:
            html = D.post(url, data = post_data)
        html = html.decode('utf-8')
        jdata = json.loads(html).get('announcements')
        if jdata:
            for i in jdata:
                bag = {}
                bag[u'关键字'] = '%s' % k.decode('utf-8')
                bag[u'代码'] = str(i.get('secCode'))
                bag[u'简称'] = i.get('secName')
                bag[u'公告标题'] =  i.get('announcementTitle')
                stime = str(i.get('announcementTime'))
                x = time.localtime(float(stime[:-3])) if stime else ''
                bag[u'公告时间'] = time.strftime('%Y-%m-%d', x)
                m = i.get('announcementId')
                bag[u'PDF文件URL'] = 'http://www.cninfo.com.cn/cninfo-new/disclosure/szse/bulletin_detail/true/' + m if m else ''
                writer.writerow(bag.get(field) for field in FIELDS)

if __name__ == '__main__':
    scrape()
