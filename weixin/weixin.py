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
    token= login(D, username, passwd)
    if not token:
        return
    stime  = raw_input('Please input the statistic time (for example: 20151025):')
    statistic_time = '-'.join([stime[:4], stime[4:6], stime[6:]])
    stime = user_scrape(D, token, statistic_time)
    txt_scrape(D, stime, token)
    all_txt_scrape(D, stime, token)

def all_txt_scrape(D, stime, token):
    url = 'https://mp.weixin.qq.com/misc/appmsganalysis?action=report&type=daily&begin_date=%s&end_date=%s&token=%s&lang=zh_CN&f=json&ajax=1'
    FIELDS = [u'采集时间', u'统计时间', u'图文页阅读人数-全部', u'图文页阅读次数-全部', u'原文页阅读人数-全部', u'原文页阅读次数-全部', u'分享转发人数-全部', u'分享转发次数-全部', u'微信收藏人数-全部', u'图文页阅读人数-会话', u'图文页阅读次数-会话', u'图文页阅读人数-好友转发', u'图文页阅读次数-好友转发', u'图文页阅读人数-朋友圈', u'图文页阅读次数-朋友圈', u'图文页阅读人数-腾讯微博', u'图文页阅读次数-腾讯微博', u'图文页阅读人数-历史消息页', u'图文页阅读次数-历史消息页', u'图文页阅读人数-其他', u'图文页阅读次数-其他']
    html = D.get(url%(stime, stime, token))
    jdata = json.loads(html)
    if 'item' not in jdata:
        return
    writer = UnicodeWriter('article_channel_info.csv', 'gbk')
    writer.writerow(FIELDS)
    us = ['99999999','0','1','2','3','4','5']
    bag = {}
    bag[u'采集时间'] = time.strftime('%Y-%m-%d')
    bag[u'统计时间'] = stime
    for i in jdata['item']:
        m = str(i['user_source'])
        assert(m in us)
        if m=='99999999':
            mindex = 2
            bag[FIELDS[mindex]] = i['int_page_read_user']
            bag[FIELDS[mindex+1]] = i['int_page_read_count']
            bag[FIELDS[mindex+2]] = i['ori_page_read_user']
            bag[FIELDS[mindex+3]] = i['ori_page_read_count']
            bag[FIELDS[mindex+4]] = i['share_user']
            bag[FIELDS[mindex+5]] = i['share_count']
            bag[FIELDS[mindex+6]] = i['add_to_fav_user']
        else:
            mindex = 2*us.index(m) + 7
            bag[FIELDS[mindex]] = i['int_page_read_user']
            bag[FIELDS[mindex+1]] = i['int_page_read_count']
    writer.writerow(bag.get(field) for field in FIELDS)

def txt_scrape(D, stime, token):
    FIELDS = [u'采集时间', u'发布时间', u'标题', u'送达人数', u'图文页阅读总人数', u'图文页阅读总次数', \
            u'原文页阅读总人数', u'原文页阅读总次数', u'转发+收藏总人数', u'转发+收藏总次数',\
            u'当日图文页阅读人数', u'当日图文页阅读次数', u'当日原文页阅读人数', u'当日原文页阅读次数',\
            u'当日转发人数', u'当日转发次数', u'当日收藏人数', u'当日收藏次数']
    writer = UnicodeWriter('article_info.csv', 'gbk')
    writer.writerow(FIELDS)
    bag = {}
    # 7 days ago
    atime = calculte_time(stime, 7)
    url ='https://mp.weixin.qq.com/misc/appmsganalysis?action=all&begin_date=%s&end_date=%s&order_by=1&order_direction=2&page_num=1&page_size=10&token=%s&lang=zh_CN&f=json&ajax=1' % (atime, stime, token)
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
        if not infos:
            print '文章发布时间超过七天，没有article_info数据'.decode('utf8').encode('gb2312')
            return
        m = jdata['total_article_data']
        m = m.replace('\\"', '"')
        m2 = json.loads(m)
        if 'list' in m2:
            for i in m2['list']:
                bag = {}
                bag[u'采集时间'] = time.strftime('%Y-%m-%d')
                bag[u'发布时间'] = i['publish_date']
                bag[u'标题'] = i['title']
                bag[u'送达人数'] = i['target_user']
                bag[u'图文页阅读总人数'] = i['int_page_read_user']
                bag[u'图文页阅读总次数'] = i['int_page_read_count']
                bag[u'原文页阅读总人数'] = i['ori_page_read_user']
                bag[u'原文页阅读总次数'] = i['ori_page_read_count']
                bag[u'转发+收藏总人数'] = str(int(i['share_user']) + int(i['add_to_fav_user']))
                bag[u'转发+收藏总次数'] = str(int(i['share_count']) + int(i['add_to_fav_count']))
                try:
                    bag[u'当日图文页阅读人数'] = infos[i['title']]['int_page_read_user']
                except KeyError:
                    continue
                bag[u'当日图文页阅读次数'] = infos[i['title']]['int_page_read_count']
                bag[u'当日原文页阅读人数'] = infos[i['title']]['ori_page_read_user']
                bag[u'当日原文页阅读次数'] = infos[i['title']]['ori_page_read_count']
                bag[u'当日转发人数'] = infos[i['title']]['share_user']
                bag[u'当日转发次数'] = infos[i['title']]['share_count']
                bag[u'当日收藏人数'] = infos[i['title']]['add_to_fav_user']
                bag[u'当日收藏次数'] = infos[i['title']]['add_to_fav_count']
                writer.writerow(bag.get(field) for field in FIELDS)

def calculte_time(stime, n):
    m = time.strptime(stime, '%Y-%m-%d')
    d = datetime.datetime(m[0], m[1], m[2])
    return (d - datetime.timedelta(days=7)).strftime('%Y-%m-%d')

def user_scrape(D, token, stime=''):
    FIELDS = [u'统计时间', u'新关注人数', u'取消关注人数', u'净增关注人数', u'累积关注人数', u'搜索公众号名称',\
            u'搜索微信号', u'图文页右上角菜单', u'名片分享', u'其他']
    writer = UnicodeWriter('user_info.csv', 'gbk')
    writer.writerow(FIELDS)
    bag = {}
    url_total = 'https://mp.weixin.qq.com/misc/useranalysis?&token=%s&lang=zh_CN'
    html = D.get(url_total% token)
    if not stime:
        m = common_re(r'\{\s*(date:\s"[^\}]+)\}\s*\]\s*\}\s*\]', html)
    else:
        m = common_re(r'\{\s*(date:\s"%s"[^\}]+)\}'% stime, html)
    bag[u'统计时间'] = common_re(r'date:\s"([^"]+)"', m) if m else ''
    bag[u'新关注人数'] = common_re(r'new_user:\s([^\s]+)\s', m) if m else ''
    bag[u'取消关注人数'] = common_re(r'cancel_user:\s([^,]+),', m) if m else ''
    bag[u'净增关注人数'] = common_re(r'netgain_user:\s([^,]+),', m) if m else ''
    bag[u'累积关注人数'] = common_re(r'cumulate_user:\s([^,]+),', m) if m else ''
    assert bag[u'统计时间']
    a = ['35', u'3', '43', '17', '0']
    b = [u'搜索公众号名称', u'搜索微信号', u'图文页右上角菜单', u'名片分享', u'其他']
    for num, i in enumerate(a):
        gain_url = 'https://mp.weixin.qq.com/misc/useranalysis?&begin_date=%s&end_date=%s&source=%s&token=%s&lang=zh_CN&f=json&ajax=1' % (bag[u'统计时间'], bag[u'统计时间'], i, token)
        gain_html = D.get(gain_url)
        bag[b[num]] = common_re(r'"new_user":([^,]+),', gain_html)
    writer.writerow(bag.get(field) for field in FIELDS)
    return bag[u'统计时间']

if __name__ == '__main__':
    scrape()
    raw_input('Finish! Please input any button to exit...')

