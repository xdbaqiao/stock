#!/usr/bin/env python2
# coding: utf-8

import sys
import base64
sys.path.append('..')

import statistics.download

'''
__xml值
0-S-0-NPHJwYyBpZD0iZHNBbGxvY2F0ZSIgdHlwZT0iQ3VzdG9tIiBvYmplY3RjbGF6ej0ibmMuYnMuaHJzcy50YS5DbG9ja2luSFZPIiBwaT0iMSIgcHM9IjEwMDAwIiBwYz0iMSIgcHJjPSIwIiBmcz0icGtfY2xvY2tpbl9oLFBLX0RJU1RMSVNULG51bSxkYXRlLHdlZWssYW1kYXRlLHBtZGF0ZSI$2BPHBzPjxwIG5hbWU9IkNZRUFSIj4yMDE1PC9wPjxwIG5hbWU9IkNQRVJJT0QiPjA3PC9wPjwvcHM$2BPHZwcz48cCBuYW1lPSJDWUVBUiIgdHlwZT0iMCI$2BMjAxNTwvcD48cCBuYW1lPSJDTU9OVEgiIHR5cGU9IjAiPjA3PC9wPjxwIG5hbWU9Il9mdW5jb2RlIiB0eXBlPSIwIj5FMDAyMDkwMjwvcD48cCBuYW1lPSJfX3Byb2ZpbGVLZXlzIiB0eXBlPSIwIj5kdEFsbG9jYXRlJTNCMDk4ODBiOTExZTdkMGE3ZDMzZGRhMDc4NjFmYjQxYWYlM0Jmb3JtMSUzQjc1NTFjOGNiNDRlMDI1Y2E0ZDAzMDI2ZmIyZWVhNWMwPC9wPjwvdnBzPjwvcnBjPg==

分割一下：
0-S-0-N
PHJwYyBpZD0iZHNBbGxvY2F0ZSIgdHlwZT0iQ3VzdG9tIiBvYmplY3RjbGF6ej0ibmMuYnMuaHJzcy50YS5DbG9ja2luSFZPIiBwaT0iMSIgcHM9IjEwMDAwIiBwYz0iMSIgcHJjPSIwIiBmcz0icGtfY2xvY2tpbl9oLFBLX0RJU1RMSVNULG51bSxkYXRlLHdlZWssYW1kYXRlLHBtZGF0ZSI
$2B
PHBzPjxwIG5hbWU9IkNZRUFSIj4yMDE1PC9wPjxwIG5hbWU9IkNQRVJJT0QiPjA3PC9wPjwvcHM
$2B
PHZwcz48cCBuYW1lPSJDWUVBUiIgdHlwZT0iMCI
$2B
MjAxNTwvcD48cCBuYW1lPSJDTU9OVEgiIHR5cGU9IjAiPjA3PC9wPjxwIG5hbWU9Il9mdW5jb2RlIiB0eXBlPSIwIj5FMDAyMDkwMjwvcD48cCBuYW1lPSJfX3Byb2ZpbGVLZXlzIiB0eXBlPSIwIj5kdEFsbG9jYXRlJTNCMDk4ODBiOTExZTdkMGE3ZDMzZGRhMDc4NjFmYjQxYWYlM0Jmb3JtMSUzQjc1NTFjOGNiNDRlMDI1Y2E0ZDAzMDI2ZmIyZWVhNWMwPC9wPjwvdnBzPjwvcnBjPg==

base64解码:
0-S-0-N
<rpc id="dsAllocate" type="Custom" objectclazz="nc.bs.hrss.ta.ClockinHVO" pi="1" ps="10000" pc="1" prc="0" fs="pk_clockin_h,PK_DISTLIST,num,date,week,amdate,pmdate"
$2B
ps><p name="CYEAR">2015</p><p name="CPERIOD">07</p></ps
$2B
vps><p name="CYEAR" type="0"
$2B
2015</p><p name="CMONTH" type="0">07</p><p name="_funcode" type="0">E0020902</p><p name="__profileKeys" type="0">dtAllocate%3B09880b911e7d0a7d33dda07861fb41af%3Bform1%3B7551c8cb44e025ca4d03026fb2eea5c0</p></vps></rpc>

修饰一下：
<rpc id="dsAllocate" type="Custom" objectclazz="nc.bs.hrss.ta.ClockinHVO" pi="1" ps="10000" pc="1" prc="0">
    <fs="pk_clockin_h,PK_DISTLIST,num,date,week,amdate,pmdate">
       <ps>
         <p name="CYEAR">2015</p>
         <p name="CPERIOD">07</p>
       </ps>
       <vps>
           <p name="CYEAR" type="0">2015</p>
           <p name="CMONTH" type="0">07</p>
           <p name="_funcode" type="0">E0020902</p>
           <p name="__profileKeys" type="0">dtAllocate%3B09880b911e7d0a7d33dda07861fb41af%3Bform1%3B7551c8cb44e025ca4d03026fb2eea5c0</p>
       </vps>
</rpc>
'''

def get_post_xml(month, year):
    data_part1 = 'ps><p name="CYEAR">%s</p><p name="CPERIOD">%s</p></ps' % (year, month)
    data_base64 = base64.b64encode(data_part1)
    data_base64 = data_base64[:-2] if data_base64.endswith('==') else data_base64
    data_part2 = '%s</p><p name="CMONTH" type="0">%s</p><p name="_funcode" type="0">E0020902</p><p name="__profileKeys" type="0">dtAllocate%3B09880b911e7d0a7d33dda07861fb41af%3Bform1%3B7551c8cb44e025ca4d03026fb2eea5c0</p></vps></rpc>' % (year, month)
    data2_base64 = base64.b64encode(data_part2)
    return '0-S-0-NPHJwYyBpZD0iZHNBbGxvY2F0ZSIgdHlwZT0iQ3VzdG9tIiBvYmplY3RjbGF6ej0ibmMuYnMuaHJzcy50YS5DbG9ja2luSFZPIiBwaT0iMSIgcHM9IjEwMDAwIiBwYz0iMSIgcHJjPSIwIiBmcz0icGtfY2xvY2tpbl9oLFBLX0RJU1RMSVNULG51bSxkYXRlLHdlZWssYW1kYXRlLHBtZGF0ZSI$2B' + data_base64 + '' +\
      '$2BPHZwcz48cCBuYW1lPSJDWUVBUiIgdHlwZT0iMCI$2B' + data2_base64

def common_re(str_re, html): m = re.compile(str_re).search(html)
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
    sso_url = 'https://sso.guosen.com.cn/Default.aspx'
    html = download().get(sso_url)
    if '您好！欢迎访问单点系统' in html:
        print 'Login sucessfully!'
        hr_url = 'https://hr.guosen.com.cn/sso/SsoHrssServlet'
        download().get(hr_url)
        end_url = 'https://hr.guosen.com.cn/hrss/ta/Clockin.jsp?_funcode=E0020902'
        post_url = 'https://hr.guosen.com.cn/hrss/dorado/smartweb2.RPC.d?__rpc=true'
        download().get(end_url)
    else:
        print 'Login fail...'

if __name__ == '__main__':
    login()
