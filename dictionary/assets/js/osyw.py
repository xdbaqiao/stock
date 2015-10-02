#!/usr/bin/env python
#coding=utf-8
import os,sys
from bottle import request,route,error,run,default_app
from bottle import template,static_file,redirect,abort
import psycopg2
import logging
import uuid
from beaker.middleware import SessionMiddleware
from bottle import TEMPLATE_PATH
import time
import hashlib
import json

#from paste import httpserver

#获取本脚本所在的路径
pro_path = os.path.split(os.path.realpath(__file__))[0]
sys.path.append(pro_path)
import setting
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
#定义错误日志路径
error_log = '/'.join((pro_path,'osyw_error.log'))


#定义数据库相关帐号信息
#db_ip = '192.168.1.9'
#db_user = 'dywl_user'
#db_pass = 'dywl@123db'
#db_name = 'dywl_select_user'
#db_port = 5432
db_ip = setting.db_ip
db_user = setting.db_user
db_pass = setting.db_pass
db_name = setting.db_name
db_port = setting.db_port

#定义日志输出格式
logging.basicConfig(level=logging.ERROR,
        format = '%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
        datefmt = '%Y-%m-%d %H:%M:%S',
        filename = error_log,
        filemode = 'a')

#定义PID路径
pid_path = '/var/run/osyw.pid'
def daemonize():
    """把本脚本转为守护进程"""
    try:
        pid=os.fork()
        if pid>0:
            sys.exit(0)
    except Exception,e:
        logging.error(e)
        sys.exit(1)

    os.chdir('/')
    os.umask(0)
    os.setsid()

    try:
        pid=os.fork()
        if pid>0:
            sys.exit(0)
    except Exception,e:
        logging.error(e)
        sys.exit(1)

    PID = str(os.getpid())
    with open(pid_path,'w') as f:
        f.write(PID)


#设置session参数
session_opts = {
    'session.type':'file',
    'session.cookei_expires':3600,
    'session.data_dir':'/tmp/sessions',
    'sessioni.auto':True
    }

def writeDb(sql):
    """
    连接mysql数据库（写），并进行写的操作
    """
    try:
        conn = psycopg2.connect(database=db_name,user=db_user,password=db_pass,host=db_ip,port=5432)
        cursor = conn.cursor()
    except Exception,e:
        print e
        logging.error(e)

    try:
        cursor.execute(sql)
        conn.commit()
    except Exception,e:
        conn.rollback()
        logging.error(e)
        return False
    finally:
        cursor.close()
        conn.close()
    return True


def readDb(sql):
    """
    连接mysql数据库（从），并进行数据查询
    """
    try:
        conn = psycopg2.connect(database=db_name,user=db_user,password=db_pass,host=db_ip,port=5432)
        cursor = conn.cursor()
    except Exception,e:
        print e
        logging.error(e)

    try:
        cursor.execute(sql)
        data = [dict((cursor.description[i][0], value or '') for i, value in enumerate(row)) for row in cursor.fetchall()]
    except Exception,e:
        logging.error(e)
        return False
    finally:
        cursor.close()
        conn.close()
    return data

@route('/')
def index():
    s = request.environ.get('beaker.session')
    if s.get('user',None) == None:
        return redirect('/login')

    return template('index')


@error(404)
def error404(error):
    """定制错误页面"""
    return '迷路了？'


@route('/assets/<filename:re:.*\.css|.*\.js|.*\.png|.*\.jpg>')
def server_static(filename):
    """定义/assets/下的静态(css,js,图片)资源路径"""
    return static_file(filename, root=assets_path)

@route('/assets/<filename:re:.*\.ttf|.*\.otf|.*\.eot|.*\.woff|.*\.svg|.*\.map>')
def server_static(filename):
    """定义/assets/字体资源路径"""
    return static_file(filename, root=assets_path)

#@route('/hosts')
#def hosts():
#    s = request.environ.get('beaker.session')
#    if s.get('user',None) == None:
#        return redirect('/login')
#    sql = 'select * from hosts order by id'
#    data = readDb(sql)
#    if data == 1:
#        return '数据查询错误！'
#    return template('hosts',host_list=data,message='')
#
#
#@route('/hosts',method = 'POST')
#def do_hosts():
#    s = request.environ.get('beaker.session')
#    if s.get('user',None) == None:
#        return redirect('/login')
#
#    wip = request.forms.get('wip')
#    nip = request.forms.get('nip')
#    hostname = request.forms.get('hostname')
#    user = request.forms.get('user')
#    port = request.forms.get('port')
#    passwd = request.forms.get('passwd')
#    idc = request.forms.get('idc')
#    note = request.forms.get('note')
#    guid = uuid.uuid1()
#    sql = "insert into hosts(wip,nip,hostname,user,port,passwd,idc,note,guid) \
#        value('%s','%s','%s','%s','%s','%s','%s','%s','%s')" \
#        % (wip,nip,hostname,user,port,passwd,idc,note,guid)
#    status = writeDb(sql)
#    if status != 0:
#        return '数据写入错误！'
#    return redirect('/hosts')
#
#@route('/delhost/<guid>')
#def delhost(guid):
#    s = request.environ.get('beaker.session')
#    if s.get('user',None) == None:
#        return redirect('/login')
#
#    try:
#        referer = request.environ.get('HTTP_REFERER').split('/')[-2]
#    except Exception:
#        abort(404)
#    #如果截取的跳转页面来自非hosts页面，则抛出404错误
#    if referer != 'hosts':
#        abort(404)
#    sql = "delete from hosts where guid='%s'" % guid
#    status = writeDb(sql)
#    if status != 0:
#        return '删除主机（SQL）失败！'
#    return redirect('/hosts')
#
#@route('/host-page/<id>')
#def host_page(id):
#    s = request.environ.get('beaker.session')
#    if s.get('user',None) == None:
#        return redirect('/login')
#    sql = 'select * from host where hid = %s' % id
#    data = readDb(sql)
#    if data == 1:
#        return '数据查询失败！'
#    print data
#    return template('host-page',host_info=data)

@route('/data')
def data():
    s = request.environ.get('beaker.session')
    if s.get('user',None) == None:
        return redirect('/login')
    #分析APP各类型下载数据
    sql = '''
        select
            download_time::date,
            sum(case when download_type='bill.apk' then 1 else 0 end) as android_bill ,
            sum(case when download_type='car.apk' then 1 else 0 end) as android_car,
            sum(case when download_type='setup.exe' then 1 else 0 end) as pc,
            sum(case when download_type='bill.ipa' then 1 else 0 end) as ios_bill,
            sum(case when download_type='car.ipa' then 1 else 0 end) as ios_car
        from download_analyze
        where
            download_time>=current_date-10
        group by download_time::date
        ORDER BY download_time::date;
    '''
    data = readDb(sql)
    if not data:
        return 'APP下载分析-数据查询失败！'
    dtime = []
    android_bill = []
    android_car = []
    pc = []
    ios_bill = []
    ios_car = []
    for i in data:
        dtime.append(i.get('download_time').strftime("%Y-%m-%d"))
        android_bill.append(str(i.get('android_bill')))
        android_car.append(str(i.get('android_car')))
        pc.append(str(i.get('pc')))
        ios_bill.append(str(i.get('ios_bill')))
        ios_car.append(str(i.get('ios_car')))

    #分析下载来源数据
    down_sql = '''
            select
                sum(case when code='0' then 1 else 0 end) as unbaidu,
                sum(case when code!='0' then 1 else 0 end) as baidu,
                current_date-1 as rq
            from download_analyze
            where
                download_time::date=current_date-1;
        '''
    data_down = readDb(down_sql)
    if not data_down:
        return '下载来源分析-数据查询失败！'
    down_dtime = data_down[0].get('rq').strftime("%Y-%m-%d")
    return template('data',dtime=dtime,android_bill=android_bill,android_car=android_car,pc=pc,ios_bill=ios_bill,ios_car=ios_car,data_down=data_down,down_dtime=down_dtime)

@route('/login')
def login():
    return template('login',message='')

@route('/login',method='POST')
def do_login():
    user = request.forms.get('user').strip()
    passwd = request.forms.get('passwd').strip()

    if not user or not passwd:
        message = u'帐号或密码不能为空！'
        return template('login',message=message)

    m = hashlib.md5()
    m.update(passwd)
    passwd_md5 = m.hexdigest()
    auth_sql = '''
        SELECT
            id,username
        FROM
            admin
        WHERE
            username='%s' and password='%s'
        ''' % (user,passwd_md5)

    auth_user = readDb(auth_sql)
    if auth_user:
        s = request.environ.get('beaker.session')
        s['user'] = user
        s['userid'] = auth_user[0]['id']
        s.save()
    else:
        message = u'帐号或密码错误！'
        return template('login',message=message)
    return redirect('/')

@route('/logout')
def logout():
    s = request.environ.get('beaker.session')
    user = s.get('user',None)
    try:
        s.delete()
    except Exception:
        pass
    return redirect('/login')

@route('/addkeyword')
def addkeyword():
    s = request.environ.get('beaker.session')
    if s.get('user',None) == None:
        return redirect('/login')
    select_sql = 'select id,sitename from promotionsite'
    data = readDb(select_sql)
    print 'data:',data
    return template('addkeyword',site_data=data)

@route('/showsite')
def addsite():
    s = request.environ.get('beaker.session')
    if s.get('user',None) == None:
        return redirect('/login')
    return template('addsite')

@route('/addsite',method='POST')
def addsite():
    s = request.environ.get('beaker.session')
    if s.get('user',None) == None:
        return redirect('/login')
    sitename = request.forms.get('sitename')
    sitenote = request.forms.get('sitenote')
    print sitenote
    print sitename
    admin_id = s.get('userid','末知')
    admin_name = s.get('user','末知')
    if not sitenote or not sitenote:
        return '-1'
    sql = """
        insert into promotionsite(sitename,sitenote) values('%s','%s')
    """ % (sitename,sitenote)
    status = writeDb(sql)
    if status:
        return '0'
    else:
        return '-1'


@route('/addkeyword',method='POST')
def addkeyword():
    s = request.environ.get('beaker.session')
    if s.get('user',None) == None:
        return redirect('/login')
    keyword = request.forms.get('keyword').strip()
    keycode = request.forms.get('keycode').strip()
    notes = request.forms.get('notes').strip()
    parentid = request.forms.get('site').strip()
    sortid = request.forms.get('sortid').strip()
    admin_id = s.get('userid','末知')
    admin_name = s.get('user','末知')
    if not keyword or not keycode or not notes or not parentid or not sortid:
        return '-1'
    sql = """
        insert into searchcode(code,code_name,notes,parentid,sortid,admin_id,admin_name) values('%s','%s','%s','%s','%s','%s','%s')
    """ % (keycode,keyword,notes,int(parentid),int(sortid),int(admin_id),admin_name)
    status = writeDb(sql)
    if status:
        return '0'
    else:
        return '-1'


@route('/changekeyword/<id>',method='POST')
def changekeyword(id):
    s = request.environ.get('beaker.session')
    if s.get('user',None) == None:
        return redirect('/login')
    keyword = request.forms.get('keyword').strip()
    keycode = request.forms.get('keycode').strip()
    notes = request.forms.get('notes').strip()
    parentid = request.forms.get('site').strip()
    sortid = request.forms.get('sortid').strip()
    admin_id = s.get('userid','末知')
    admin_name = s.get('user','末知')
    if not keyword or not keycode or not notes or not parentid or not sortid:
        return '-1'
    
    update_sql = """
        update searchcode set code='%s',code_name='%s',notes='%s',parentid='%s',sortid='%s',admin_id='%s',admin_name='%s' where id='%s'
    """ % (keycode,keyword,notes,int(parentid),int(sortid),int(admin_id),admin_name,id)
    status = writeDb(update_sql)
    if status:
        return '0'
    else:
        return '-1'

@route('/changesite/<id>',method='POST')
def changesite(id):
    s = request.environ.get('beaker.session')
    if s.get('user',None) == None:
        return redirect('/login')
    sitename = request.forms.get('sitename').strip()
    sitenote = request.forms.get('sitenote').strip()
    admin_id = s.get('userid','末知')
    admin_name = s.get('user','末知')
    if not sitename or not sitenote:
        return '-1'
    
    update_sql = """
        update promotionsite set sitename='%s',sitenote='%s' where id='%s'
    """ % (sitename,sitenote,id)
    status = writeDb(update_sql)
    if status:
        return '0'
    else:
        return '-1'



@route('/delkeyword',method='POST')
def delkeyword():
    s = request.environ.get('beaker.session')
    if s.get('user',None) == None:
        return redirect('/login')
    id = request.forms.get('str').rstrip(',')
    if not id:
        return '-1'
    del_sql = "delete from searchcode where id in (%s)" % id
    status = writeDb(del_sql)
    if status:
        return '0'
    else:
        return '-1'

@route('/delsite',method='POST')
def delsite():
    s = request.environ.get('beaker.session')
    if s.get('user',None) == None:
        return redirect('/login')
    id = request.forms.get('str').rstrip(',')
    if not id:
        return '-1'
    del_sql = "delete from promotionsite where id in (%s)" % id
    status = writeDb(del_sql)
    if status:
        return '0'
    else:
        return '-1'


@route('/api/getkeyword',method='POST')
def getkeyword():
    s = request.environ.get('beaker.session')
    if s.get('user',None) == None:
        return redirect('/login')
    sql = """
        select s.id,s.code,s.code_name,s.notes,p.sitename as parentid,s.sortid,s.admin_id,s.admin_name from searchcode as s left join promotionsite as p on s.parentid=p.id
    """
    data = readDb(sql)
    return json.dumps(data)

@route('/api/getsite',method='POST')
def getsite():
    s = request.environ.get('beaker.session')
    if s.get('user',None) == None:
        return redirect('/login')
    sql = """
        select id,sitename,sitenote from promotionsite
    """
    data = readDb(sql)
    return json.dumps(data)


@route('/appdata')
def appdata():
    s = request.environ.get('beaker.session')
    if s.get('user',None) == None:
        return redirect('/login')
    sql = '''
         select
               t.addtime,
               (select count(1) from sys_login_info WHERE (sys_login_info.apptype='10' OR sys_login_info.apptype='12') AND sys_login_info.addtime::date=t.addtime) AS azf,
               (select count(1) from sys_login_info WHERE (sys_login_info.apptype='11' OR sys_login_info.apptype='13') AND sys_login_info.addtime::date=t.addtime) AS azy,
               (select count(1) from sys_login_info WHERE (sys_login_info.apptype='20' OR sys_login_info.apptype='22') AND sys_login_info.addtime::date=t.addtime) AS ipf,
               (select count(1) from sys_login_info WHERE (sys_login_info.apptype='21' OR sys_login_info.apptype='23') AND sys_login_info.addtime::date=t.addtime) AS ipy,
               (select count(1) from sys_login_info WHERE (sys_login_info.apptype='50') AND sys_login_info.addtime::date=t.addtime) AS web,
               (select count(1) from sys_login_info WHERE (sys_login_info.apptype='40') AND sys_login_info.addtime::date=t.addtime) AS pc,
               (select count(1) from sys_login_info WHERE (sys_login_info.apptype='60') AND sys_login_info.addtime::date=t.addtime) AS wap

        FROM (

        SELECT 
                
                addtime::date AS addtime							
            
        FROM
            sys_login_info
        WHERE
            addtime::date = current_date-30) as t       
    '''
    data = readDb(sql)
    for i in data:
        print i
    return template('appdata')

if __name__ == '__main__':
#    daemonize()
    #run(host='0.0.0.0', port=80,debug=True,)
    #httpserver.serve(default_app(), host='0.0.0.0', port = 80)
    app = default_app()
    app = SessionMiddleware(app, session_opts)
    run(app=app,host='0.0.0.0', port=8080,debug=True)
