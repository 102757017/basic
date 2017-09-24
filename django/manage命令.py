#!/usr/bin/python
# -*- coding: UTF-8 -*-
import os
import sys
import django

print("当前脚本工作的目录路径:")
path1=os.getcwd()
print(path1)
print('\n')

print("切换工作目录")
#此处的mysite为项目名称
path2=sys.path[0]+os.path.sep+"mysite"
os.chdir(path2)
print("切换后脚本工作的目录路径:")
path1=os.getcwd()
print(path1)


#载入django设定后启动shell
c1='sh & '
#c2="python manage.py shell"
c2=sys.executable+" "+"manage.py shell"

#运行mysite目录下的开发服务器
#c2=sys.executable+" "+"manage.py runserver"
'''
现在用网页浏览器访问 http://127.0.0.1:8000/ 。
应该可以看到一个令人赏心悦目的淡蓝色Django欢迎页面。 它开始工作了。
'''


#创建一个app
#c2=sys.executable+" "+"manage.py startapp myapp"

#自动进入在settings.py中设置的数据库
#c2=sys.executable+" "+"manage.py dbshell"

#探测数据库的结构，自动构造modul
#c2=sys.executable+" "+"manage.py inspectdb > myapp/models.py"


#将model层转为迁移文件migration
#c2=sys.executable+" "+"manage.py makemigrations"

#查看数据库同步的sql语句
#c2=sys.executable+" "+"manage.py sqlmigrate myapp 0003_auto_20170919_1721"

#将新版本的迁移文件执行，更新数据库
#c2=sys.executable+" "+"manage.py migrate"

#检查django项目完整性
#c2=sys.executable+" "+"manage.py check"

#清空数据库
#c2=sys.executable+" "+"manage.py flush"
c=c1+c2
os.system(c)

