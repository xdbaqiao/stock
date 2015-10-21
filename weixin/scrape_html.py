#!/usr/bin/env python2
# coding: utf-8

import os
import time
import datetime
import json
from common import common_re, UnicodeWriter
from login import login
from download  import download

def scrape():
    refer_url = 'https://mp.weixin.qq.com/'
    D = download(first_url=refer_url, is_cookie=True)
    username = os.environ.get('WX_username')
    passwd = os.environ.get('WX_passwd')
    if not login(D, username, passwd):
        return
    stime = user_scrape(D)
    txt_scrape(D, stime)
    all_txt_scrape(D, stime)

def all_txt_scrape(D, stime):
    url = 'https://mp.weixin.qq.com/misc/appmsganalysis?action=report&token=195186981&lang=zh_CN'
    html = D.get(url)
    bag = {}
    bag['统计时间'] = time.strftime('%Y-%m-%d')

def txt_scrape(D, stime):
    FIELDS = ['统计时间', '发布时间', '标题', '送达人数', '图文页阅读总人数', '图文页阅读总次数', \
            '原文页阅读总人数', '原文页阅读总次数', '转发+收藏总人数', '转发+收藏总次数',\
            '当日图文页阅读人数', '当日图文页阅读次数', '当日原文页阅读人数', '当日原文页阅读次数',\
            '当日转发人数', '当日转发次数', '当日收藏人数', '当日收藏次数']
    writer = UnicodeWriter('article_info.csv')
    writer.writerow(FIELDS)
    bag = {}
    # 7 days ago
    atime = calculte_time(stime, 7)
    url ='https://mp.weixin.qq.com/misc/appmsganalysis?action=all&begin_date=%s&end_date=%s&order_by=1&order_direction=2&page_num=1&page_size=10&token=195186981&lang=zh_CN&f=json&ajax=1' % (atime, stime)
    html = D.get(url)
    jdata = json.loads(html)
    if 'total_article_data' in jdata:
        infos = {}
        m = jdata['article_summary_data']
        m = m.replace('\\"', '"')
        m2 = json.loads(m)
        if 'list' in m2:
            for i in m2['list']:
                if i['ref_date'] == stime:
                    infos[i['title']] = i
        m = jdata['total_article_data']
        m = m.replace('\\"', '"')
        m2 = json.loads(m)
        if 'list' in m2:
            for i in m2['list']:
                bag = {}
                bag['统计时间'] = time.strftime('%Y-%m-%d')
                bag['发布时间'] = i['publish_date']
                bag['标题'] = i['title']
                bag['送达人数'] = i['target_user']
                bag['图文页阅读总人数'] = i['int_page_read_user']
                bag['图文页阅读总次数'] = i['int_page_read_count']
                bag['原文页阅读总人数'] = i['ori_page_read_user']
                bag['原文页阅读总次数'] = i['ori_page_read_count']
                bag['转发+收藏总人数'] = str(int(i['share_user']) + int(i['add_to_fav_user']))
                bag['转发+收藏总次数'] = str(int(i['share_count']) + int(i['add_to_fav_count']))
                bag['当日图文页阅读人数'] = infos[i['title']]['int_page_read_user']
                bag['当日图文页阅读次数'] = infos[i['title']]['int_page_read_count']
                bag['当日原文页阅读人数'] = infos[i['title']]['ori_page_read_user']
                bag['当日原文页阅读次数'] = infos[i['title']]['ori_page_read_count']
                bag['当日转发人数'] = infos[i['title']]['share_user']
                bag['当日转发次数'] = infos[i['title']]['share_count']
                bag['当日收藏人数'] = infos[i['title']]['add_to_fav_user']
                bag['当日收藏次数'] = infos[i['title']]['add_to_fav_count']
                writer.writerow(bag.get(field) for field in FIELDS)

def calculte_time(stime, n):
    m = time.strptime(stime, '%Y-%m-%d')
    d = datetime.datetime(m[0], m[1], m[2])
    return (d - datetime.timedelta(days=7)).strftime('%Y-%m-%d')

def user_scrape(D):
    FIELDS = ['时间', '新关注人数', '取消关注人数', '净增关注人数', '累积关注人数', '搜索公众号名称',\
            '搜索微信号', '图文页右上角菜单', '名片分享', '其他']
    writer = UnicodeWriter('user_info.csv')
    writer.writerow(FIELDS)
    bag = {}
    url_total = 'https://mp.weixin.qq.com/misc/useranalysis?&token=195186981&lang=zh_CN'
    html = D.get(url_total)
    m = common_re(r'\{\s*(date:\s"[^\}]+)\}\s*\]\s*\}\s*\]', html)
    bag['时间'] = common_re(r'date:\s"([^"]+)"', m) if m else ''
    bag['新关注人数'] = common_re(r'new_user:\s([^\s]+)\s', m) if m else ''
    bag['取消关注人数'] = common_re(r'cancel_user:\s([^,]+),', m) if m else ''
    bag['净增关注人数'] = common_re(r'netgain_user:\s([^,]+),', m) if m else ''
    bag['累积关注人数'] = common_re(r'cumulate_user:\s([^,]+),', m) if m else ''
    assert bag['时间']
    a = ['35', '3', '43', '17', '0']
    b = ['搜索公众号名称', '搜索微信号', '图文页右上角菜单', '名片分享', '其他']
    for num, i in enumerate(a):
        gain_url = 'https://mp.weixin.qq.com/misc/useranalysis?&begin_date=%s&end_date=%s&source=%s&token=195186981&lang=zh_CN&f=json&ajax=1' % (bag['时间'], bag['时间'], i)
        gain_html = D.get(gain_url)
        bag[b[num]] = common_re(r'"new_user":([^,]+),', gain_html)
    writer.writerow(bag.get(field) for field in FIELDS)
    return bag['时间']

if __name__ == '__main__':
    scrape()
