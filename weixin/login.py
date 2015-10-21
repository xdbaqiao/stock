#!/usr/bin/env python2
# coding: utf-8

import sys 
import re
import os
from download import download
from common import common_re


def login(D, username, passwd):
    url = 'https://mp.weixin.qq.com/'
    print username, passwd



if __name__ == '__main__':
    D = download()
    username = os.environ.get('WX_username')
    passwd = os.environ.get('WX_passwd')
    login(D, username, passwd)
