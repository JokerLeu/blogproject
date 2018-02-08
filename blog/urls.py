"""
blog的url配置
创建者：jokerleu
"""
from django.urls import path, re_path  # 正常url，正则url

from . import views

app_name = 'blog'  # 与根url不同，此为视图函数命名空间
urlpatterns = [
    re_path('^$', views.IndexView.as_view(), name='index'),  # 新，用as_view()将IndexView转换成视图
    # re_path('^$', views.index, name='index'),  # 旧
    re_path('^post/(?P<pk>[0-9]+)/$', views.PostDetailView.as_view(), name='detail'),
    re_path('^archives/(?P<year>[0-9]{4})/(?P<month>[0-9]{1,2})/$', views.ArchivesView.as_view(), name='archives'),
    re_path('^category/(?P<pk>[0-9]+)/$', views.CategoryView.as_view(), name='category'),
    # re_path('^category/(?P<pk>[0-9]+)/$', views.category, name='category'),  # 旧
    re_path('^tag/(?P<pk>[0-9]+)/$', views.TagView.as_view(), name='tag'),
    # re_path('^search/$', views.search, name='search'),  # 搜索的URL——旧
]
