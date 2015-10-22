#!/usr/bin/env python2
# coding: utf-8

import os
import hashlib
from download import download
from common import common_re

def login(D, username, passwd):
    url = 'https://mp.weixin.qq.com/cgi-bin/login'
    post_data = {}
    post_data['username'] = username
    m = hashlib.md5()
    m.update(passwd)
    post_data['pwd'] = m.hexdigest()
    post_data['imgcode'] = ''
    post_data['f'] = 'json'
    m = D.post(url, data=post_data)
    token = common_re(r'token=([^"]+)"', m)
    url =  'https://mp.weixin.qq.com/cgi-bin/home?t=home/index&lang=zh_CN&token=%s' % token
    html = D.get(url)
    if 'success">已认证' in html:
        print 'Login succefully!'
        return token 
    else:
        print 'Login fail.'
        return False

if __name__ == '__main__':
    refer_url = 'https://mp.weixin.qq.com/'
    D = download(first_url=refer_url, is_cookie=True)
    username = os.environ.get('WX_username')
    passwd = os.environ.get('WX_passwd')
    login(D, username, passwd)
