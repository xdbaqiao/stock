#!/usr/bin/env python2
# coding: utf-8

import sys
import re
from common import common_re

sys.path.append('..')

import statistics.download

def login(userid, passwd, dynamic_passwd):
    url = 'https://sso.guosen.com.cn/Login.aspx'
    D = download(is_cookie=True)
    html = D.get(url)
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
    html = D.post(url, post_data)
    sso_url = 'https://sso.guosen.com.cn/Default.aspx'
    login_data = {}
    login_data['IASID'] = common_re(r'"IASID"[^>]+value="([^"]+)"', html)
    login_data['Result'] = '0' 
    login_data['TimeStamp'] = common_re(r'"TimeStamp"[^>]+value="([^"]+)"', html)
    login_data['UserAccount'] = userid
    login_data['ErrorDescription'] = ''
    login_data['Authenticator'] = common_re(r'"Authenticator"[^>]+value="([^"]+)"', html)
    login_data['IASUserAccount'] = userid
    html = D.post(sso_url, login_data)    
    if '您好！欢迎访问单点系统' in html and '<span id="lblCurrentUser"></span>' not in html:
        print 'Login sucessfully!'
        return True
    else:
        print 'Login fail...'
        return False

if __name__ == '__main__':
    login()
