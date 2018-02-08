"""blogproject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.http import HttpResponse  # 用于爬虫声明

from blog.feeds import AllPostsRssFeed  # 引入RSS订阅

urlpatterns = [
    path('admin/', admin.site.urls),
    # blog的url
    path('', include('blog.urls')),  # 引入blog的url
    # comment的url
    path('', include('comments.urls')),  # 引入comments的url
    # RSS订阅的url
    path('all/rss/', AllPostsRssFeed(), name='rss'),
    # blog搜索的url
    path('search/', include('haystack.urls')),
    # 爬虫声明 lambda 输入：输出
    path('robots.txt', lambda r: HttpResponse('User-agent: *\nDisallow: /', content_type='text/plain'))
]
