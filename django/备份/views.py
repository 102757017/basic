# -*- coding: UTF-8 -*-
from django.http import HttpResponse
from django.template import Template, Context
from django.template.loader import get_template
from django.shortcuts import render_to_response
import sys
import datetime
sys.path.append(r'F:\学习资料\编程学习\pathon\django\mysite')

def static(request):
    return render_to_response('static.html')

def hello(request):
    html = "<html><body>Hello world</body></html>"
    return HttpResponse(html)


#使用模板的范例
def current_datetime(request):
    now = datetime.datetime.now()
    t = Template("<html><body>It is now {{ current_date }}.</body></html>")
    html = t.render(Context({'current_date': now}))
    return HttpResponse(html)

'''
从文件中加载模板，但是首先要在settings.py中设置模板路径
get_template() 方法可以直接得到Template 实例,
但是这个不是django.template.Template实例,因此render的方法不同
'''
def current_datetime2(request):
    now = datetime.datetime.now()
    t = get_template('current_datetime.html')
    html = t.render({'current_date': now})
    return HttpResponse(html)


#更快捷的写法
def current_datetime3(request):
    now = datetime.datetime.now()
    return render_to_response('current_datetime.html', {'current_date': now})
