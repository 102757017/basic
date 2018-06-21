"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
import sys
import os
a=os.path.dirname(__file__)
a=os.path.dirname(a)
sys.path.append(a)
from mysite.views import main
from mysite.views import apicouple
from mysite.views import worthygoods
from mysite.views import redpackage
from mysite.views import hello
from mysite.views import current_datetime
from mysite.views import current_datetime2
from mysite.views import current_datetime3
from mysite.views import zhuankeba
from mysite.views import jd
from mysite.views import jd24

urlpatterns = [
    url(r'^main/', main),
    url(r'^admin/', admin.site.urls),
    url('^hello/$', hello),
    url('^apicouple/$', apicouple),
    url('^worthygoods/$', worthygoods),
    url('^redpackage/$', redpackage),
    url('^current_datetime/$', current_datetime),
    url('^current_datetime2/$', current_datetime2),
    url('^current_datetime3/$', current_datetime3),
    url('^zkb/$', zhuankeba),
    url('^jd/$', jd),
    url('^jd24/$', jd24),
]
