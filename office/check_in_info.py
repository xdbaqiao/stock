#!/usr/bin/env python2
# coding: utf-8

import base64

'''
post表单中有一个字段_xml是加密过的，从最后两个值是等号猜测是base64编码，据此做一下分析：
__xml值
0-S-0-NPHJwYyBpZD0iZHNBbGxvY2F0ZSIgdHlwZT0iQ3VzdG9tIiBvYmplY3RjbGF6ej0ibmMuYnMuaHJzcy50YS5DbG9ja2luSFZPIiBwaT0iMSIgcHM9IjEwMDAwIiBwYz0iMSIgcHJjPSIwIiBmcz0icGtfY2xvY2tpbl9oLFBLX0RJU1RMSVNULG51bSxkYXRlLHdlZWssYW1kYXRlLHBtZGF0ZSI$2BPHBzPjxwIG5hbWU9IkNZRUFSIj4yMDE1PC9wPjxwIG5hbWU9IkNQRVJJT0QiPjA3PC9wPjwvcHM$2BPHZwcz48cCBuYW1lPSJDWUVBUiIgdHlwZT0iMCI$2BMjAxNTwvcD48cCBuYW1lPSJDTU9OVEgiIHR5cGU9IjAiPjA3PC9wPjxwIG5hbWU9Il9mdW5jb2RlIiB0eXBlPSIwIj5FMDAyMDkwMjwvcD48cCBuYW1lPSJfX3Byb2ZpbGVLZXlzIiB0eXBlPSIwIj5kdEFsbG9jYXRlJTNCMDk4ODBiOTExZTdkMGE3ZDMzZGRhMDc4NjFmYjQxYWYlM0Jmb3JtMSUzQjc1NTFjOGNiNDRlMDI1Y2E0ZDAzMDI2ZmIyZWVhNWMwPC9wPjwvdnBzPjwvcnBjPg==
直接解析得到乱码：
分割一下：
0-S-0-N
PHJwYyBpZD0iZHNBbGxvY2F0ZSIgdHlwZT0iQ3VzdG9tIiBvYmplY3RjbGF6ej0ibmMuYnMuaHJzcy50YS5DbG9ja2luSFZPIiBwaT0iMSIgcHM9IjEwMDAwIiBwYz0iMSIgcHJjPSIwIiBmcz0icGtfY2xvY2tpbl9oLFBLX0RJU1RMSVNULG51bSxkYXRlLHdlZWssYW1kYXRlLHBtZGF0ZSI
$2B
PHBzPjxwIG5hbWU9IkNZRUFSIj4yMDE1PC9wPjxwIG5hbWU9IkNQRVJJT0QiPjA3PC9wPjwvcHM
$2B
PHZwcz48cCBuYW1lPSJDWUVBUiIgdHlwZT0iMCI
$2B
MjAxNTwvcD48cCBuYW1lPSJDTU9OVEgiIHR5cGU9IjAiPjA3PC9wPjxwIG5hbWU9Il9mdW5jb2RlIiB0eXBlPSIwIj5FMDAyMDkwMjwvcD48cCBuYW1lPSJfX3Byb2ZpbGVLZXlzIiB0eXBlPSIwIj5kdEFsbG9jYXRlJTNCMDk4ODBiOTExZTdkMGE3ZDMzZGRhMDc4NjFmYjQxYWYlM0Jmb3JtMSUzQjc1NTFjOGNiNDRlMDI1Y2E0ZDAzMDI2ZmIyZWVhNWMwPC9wPjwvdnBzPjwvcnBjPg==

对特殊的位置进行base64解码:
0-S-0-N
<rpc id="dsAllocate" type="Custom" objectclazz="nc.bs.hrss.ta.ClockinHVO" pi="1" ps="10000" pc="1" prc="0" fs="pk_clockin_h,PK_DISTLIST,num,date,week,amdate,pmdate"
$2B
ps><p name="CYEAR">2015</p><p name="CPERIOD">07</p></ps
$2B
vps><p name="CYEAR" type="0"
$2B
2015</p><p name="CMONTH" type="0">07</p><p name="_funcode" type="0">E0020902</p><p name="__profileKeys" type="0">dtAllocate%3B09880b911e7d0a7d33dda07861fb41af%3Bform1%3B7551c8cb44e025ca4d03026fb2eea5c0</p></vps></rpc>

修饰一下,得到结果：
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
反推可以得到post编码数据
'''

def get_post_xml(month, year):
    data_part1 = 'ps><p name="CYEAR">%s</p><p name="CPERIOD">%s</p></ps' % (year, month)
    data_base64 = base64.b64encode(data_part1)
    data_base64 = data_base64[:-2] if data_base64.endswith('==') else data_base64
    data_part2 = '%s</p><p name="CMONTH" type="0">%s</p><p name="_funcode" type="0">E0020902</p><p name="__profileKeys" type="0">dtAllocate%%3B09880b911e7d0a7d33dda07861fb41af%%3Bform1%%3B7551c8cb44e025ca4d03026fb2eea5c0</p></vps></rpc>' % (year, month)
    data2_base64 = base64.b64encode(data_part2)
    return '0-S-0-NPHJwYyBpZD0iZHNBbGxvY2F0ZSIgdHlwZT0iQ3VzdG9tIiBvYmplY3RjbGF6ej0ibmMuYnMuaHJzcy50YS5DbG9ja2luSFZPIiBwaT0iMSIgcHM9IjEwMDAwIiBwYz0iMSIgcHJjPSIwIiBmcz0icGtfY2xvY2tpbl9oLFBLX0RJU1RMSVNULG51bSxkYXRlLHdlZWssYW1kYXRlLHBtZGF0ZSI$2B' + data_base64 + '' +\
      '$2BPHZwcz48cCBuYW1lPSJDWUVBUiIgdHlwZT0iMCI$2B' + data2_base64
