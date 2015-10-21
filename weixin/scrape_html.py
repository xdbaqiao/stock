#!/usr/bin/env python2
# coding: utf-8

import os
from common import common_re, UnicodeWriter
from login import login
from download  import download

def user_scrape():
    FIELDS = ['时间', '新关注人数', '取消关注人数', '净增关注人数', '累积关注人数', '搜索公众号名称',\
            '搜索微信号', '图文页右上角菜单', '名片分享', '其他']
    writer = UnicodeWriter('user_info.csv')
    writer.writerow(FIELDS)

    refer_url = 'https://mp.weixin.qq.com/'
    D = download(first_url=refer_url, is_cookie=True)
    username = os.environ.get('WX_username')
    passwd = os.environ.get('WX_passwd')
    if not login(D, username, passwd):
        return
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

if __name__ == '__main__':
    user_scrape()
