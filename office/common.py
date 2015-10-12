#!/usr/bin/env python2
# coding: utf-8

import re

def common_re(str_re, html):
    m = re.compile(str_re).search(html)
    if m:
        return m.groups()[0]
    return ''
