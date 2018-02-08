"""
RSS(Really Simple Syndication)订阅文档

创建者：jokerleu
"""
from django.contrib.syndication.views import Feed  # RSS相关的模块

from .models import Post  # 引用文章模型


class AllPostsRssFeed(Feed):
    # 显示在RSS聚合阅读器上的标题
    title = 'Django Blog'
    # 通过聚合阅读器转到的网址
    link = '/'
    # 显示在聚合阅读器上的描述信息
    description = "Django Blog Test"

    # 需要显示的内容条目
    def items(self, item):
        return Post.objects.all()

    # 聚合阅读器中内容条目的标题
    def item_title(self, item):
        return '[%s] %s' % (item.category, item.title)

    # 聚合阅读器中内容条目的描述
    def item_description(self, item):
        return item.body
