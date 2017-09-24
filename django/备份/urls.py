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
sys.path.append(r'F:\学习资料\编程学习\pathon\django\mysite')
from mysite.views import static
from mysite.views import hello
from mysite.views import current_datetime
from mysite.views import current_datetime2
from mysite.views import current_datetime3

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url('^hello/$', hello),
    url('^static/$', static),
    url('^current_datetime/$', current_datetime),
    url('^current_datetime2/$', current_datetime2),
    url('^current_datetime3/$', current_datetime3),
]
