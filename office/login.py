#!/usr/bin/env python2
# coding: utf-8

import sys
sys.path.append('..')

import statistics.download


def common_re(str_re, html):
    m = re.compile(str_re).search(html)
    if m:
        return m.groups()[0]
    return ''

def login(userid, passwd, dynamic_passwd):
    url = 'https://sso.guosen.com.cn/Login.aspx'
    html = download().get(url)
    post_data = {}
    post_data['__LASTFOCUS'] = ''
    post_data['__VIEWSTATE'] = common_re(r'id="__VIEWSTATE"\s*value="([^"]+)"', html)
    post_data['__EVENTTARGET'] = common_re(r'id="__EVENTTARGET"\s*value="([^"]+)"', html)
    post_data['__EVENTARGUMENT'] = common_re(r'id="__EVENTARGUMENT"\s*value="([^"]+)"', html)
    post_data['__EVENTVALIDATION'] = common_re(r'id="__EVENTVALIDATION"\s*value="([^"]+)"', html)
    post_data['hidReturnUrl'] = 'Default.aspx'
    post_data['hidIASID'] = '000'
    post_data['txtUserName'] = userid
    post_data['chkRememberAccount'] = 'on'
    post_data['txtPassword'] = passwd
    post_data['chkEnableDynamicCode'] = 'on'
    post_data['txtDynamicPassword'] = dynamic_passwd
    post_data['hidSms'] = '0'
    post_data['txtValidateCode'] =  ''
    post_data['btnLogin.x'] = '0'
    post_data['btnLogin.y'] =  '0'
    html = download().post(url, post_data)
