#!/usr/bin/env python
#coding=utf-8

import os,sys,json
from bottle import request,route,error,run,default_app
from bottle import template,static_file,redirect,abort
import bottle
import logging
from beaker.middleware import SessionMiddleware
from bottle import TEMPLATE_PATH
import time,datetime
import hashlib
from gevent import monkey;
import MySQLdb
import hashlib
monkey.patch_all()

db_name = 'dictionary'
db_user = 'root'
db_pass = 'youandme'
db_ip = 'localhost'
db_port = 3306

#admin
#admin,,,Ox
#db_name = os.environ.get('DD_DB_NAME') or 'dictionary'
#db_user = os.environ.get('DD_DB_USERNAME')
#db_pass = os.environ.get('DD_DB_PASSWORD')
#db_ip = os.environ.get('DD_DB_IP') or 'localhost'
#db_port = os.environ.get('DD_DB_PORT') or '3306'

#获取本脚本所在的路径
pro_path = os.path.split(os.path.realpath(__file__))[0]
sys.path.append(pro_path)

#定义assets路径，即静态资源路径，如css,js,及样式中用到的图片等
assets_path = '/'.join((pro_path,'assets'))

#定义图片路径
images_path = '/'.join((pro_path,'images'))

#定义提供文件下载的路径
download_path = '/'.join((pro_path,'download'))

#定义文件上传存放的路径
upload_path = '/'.join((pro_path,'upload'))

#定义模板路径
TEMPLATE_PATH.append('/'.join((pro_path,'views')))

#定义日志目录
log_path = ('/'.join((pro_path,'log')))

#定义日志输出格式
logging.basicConfig(level=logging.ERROR,
        format = '%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
        datefmt = '%Y-%m-%d %H:%M:%S',
        filename = "%s/error_log" % log_path,
        filemode = 'a')

def writeDb(sql,db_data=()):
    """
    连接mysql数据库（写），并进行写的操作
    """
    try:
        conn = MySQLdb.connect(db=db_name,user=db_user,passwd=db_pass,host=db_ip,port=int(db_port))
        cursor = conn.cursor()
    except Exception,e:
        print e
        logging.error('数据库连接失败:%s' % e)
        return False

    try:
        cursor.execute(sql,db_data)
        conn.commit()
    except Exception,e:
        conn.rollback()
        logging.error('数据写入失败:%s' % e)
        return False
    finally:
        cursor.close()
        conn.close()
    return True


def readDb(sql,db_data=()):
    """
    连接mysql数据库（从），并进行数据查询
    """
    try:
        conn = MySQLdb.connect(db=db_name,user=db_user,passwd=db_pass,host=db_ip,port=int(db_port))
        cursor = conn.cursor()
    except Exception,e:
        print e
        logging.error('数据库连接失败:%s' % e)
        return False

    try:
        cursor.execute(sql,db_data)
        data = [dict((cursor.description[i][0], value) for i, value in enumerate(row)) for row in cursor.fetchall()]
    except Exception,e:
        logging.error('数据执行失败:%s' % e)
        return False
    finally:
        cursor.close()
        conn.close()
    return data


#设置session参数
session_opts = {
    'session.type':'file',
    'session.cookei_expires':3600,
    'session.data_dir':'/tmp/sessions',
    'sessioni.auto':True
    }

def checkLogin(fn):
    """验证登陆，如果没有登陆，则跳转到login页面"""
    def BtnPrv(*args,**kw):
        s = request.environ.get('beaker.session')
        if not s.get('userid',None):
            return redirect('/login')
        return fn(*args,**kw)
    return BtnPrv

def checkAccess(fn):
    """验证权限，如果非管理员权限，则返回404页面"""
    def BtnPrv(*args,**kw):
        s = request.environ.get('beaker.session')
        if not s.get('userid',None):
            return redirect('/login')
        elif s.get('access',None) != 1:
            abort(404)
        return fn(*args,**kw)
    return BtnPrv

@error(404)
def error404(error):
    """定制错误页面"""
    return template('404')

@route('/assets/<filename:re:.*\.css|.*\.js|.*\.png|.*\.jpg|.*\.gif>')
def server_static(filename):
    """定义/assets/下的静态(css,js,图片)资源路径"""
    return static_file(filename, root=assets_path)

@route('/assets/<filename:re:.*\.ttf|.*\.otf|.*\.eot|.*\.woff|.*\.svg|.*\.map>')
def server_static(filename):
    """定义/assets/字体资源路径"""
    return static_file(filename, root=assets_path)

@route('/')
@route('/dictionary')
@checkLogin
@checkAccess
def dictionary():
    department_sql = "select id,dkey from dictionary;"
    department_result = readDb(department_sql,)
    message = ''
    return template('dictionary',department_result=department_result, message=message)

@route('/adddict',method="POST")
@checkAccess
def adddict():
    key = request.forms.get("dkey")
    value = request.forms.get("dvalue")
    table = request.forms.get("dtable")
    comment = request.forms.get("comment")

    if not (key and value):
        message = "表单不允许为空！"
        return '-2'
    sql = """
            INSERT INTO
                dictionary(dkey,dvalue,dtable,comment)
            VALUES(%s,%s,%s,%s)
        """
    data = (key, value, table, comment)
    result = writeDb(sql,data)
    if result:
        return '0'
    else:
        return '-1'

@route('/changedict/<id>',method="POST")
@checkAccess
def changedict(id):
    dkey = request.forms.get("dkey")
    dvalue = request.forms.get("dvalue")
    dtable = request.forms.get("dtable")
    comment = request.forms.get("comment")

    def checkRequest(list_data):
        for i in list_data:
            if not i.strip():
                return '-2'

    if not (dvalue and dkey):
        message = "表单不允许为空！"
        return '-2'

    sql = """
            UPDATE dictionary SET
            dvalue=%s,dtable=%s,comment=%s
            WHERE dkey=%s
        """
    data = (dvalue, dtable, comment, dkey)
    result = writeDb(sql,data)
    if result:
        return '2'
    else:
        return '3'

@route('/deldict',method="POST")
@checkAccess
def deldict():
    id = request.forms.get('str').rstrip(',')
    if not id:
        return '-1'
    id_all = ids.split(',')
    sql = """delete from dictionary where dkey in (%s)""" % ','.join(['%s']*len(id_all))
    result = writeDb(sql, tuple(id_all))
    if result:
        return '0'
    else:
        return '-1'

@route('/api/getdict',method=['GET', 'POST'])
@checkAccess
def getdict():
    sql = """
    SELECT
        dkey,
        dvalue,
        dtable,
        comment,
        date_format(adddate,'%%Y-%%m-%%d %%H:%%i:%%s') as adddate
    FROM
        dictionary
    """
    userlist = readDb(sql,)
    return json.dumps(userlist)

@route('/login')
def login():
    """用户登陆"""
    return template('login',message='')

@route('/login',method='POST')
def do_login():
    """用户登陆过程，判断用户帐号密码，保存SESSION"""
    username = request.forms.get('username').strip()
    passwd = request.forms.get('passwd').strip()
    if not username or not passwd:
        message = u'帐号或密码不能为空！'
        return template('login',message=message)

    m = hashlib.md5()
    m.update(passwd)
    passwd_md5 = m.hexdigest()
    auth_sql = '''
        SELECT
            id,username,name,access
        FROM
            user
        WHERE
            username=%s and passwd=%s
        '''
    auth_user = readDb(auth_sql,(username,passwd_md5))
    if auth_user:
        s = request.environ.get('beaker.session')
        s['username'] = username
        s['name'] = auth_user[0]['name']
        s['userid'] = auth_user[0]['id']
        s['access'] = auth_user[0]['access']
        s.save()
    else:
        message = u'帐号或密码错误！'
        return template('login',message=message)
    return redirect('/dictionary')

@route('/logout')
@checkLogin
def logout():
    """退出系统"""
    s = request.environ.get('beaker.session')
    user = s.get('user',None)
    try:
        s.delete()
    except Exception:
        pass
    return redirect('/login')

if __name__ == '__main__':
    app = default_app()
    app = SessionMiddleware(app, session_opts)
    run(app=app,host='0.0.0.0', port=8080,debug=True,server='gevent')
else:
    application = SessionMiddleware(default_app(), session_opts)
