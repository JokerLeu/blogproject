"""
自定义模板标签文件

创建者：jokerleu
"""
from django import template
from django.db.models.aggregates import Count  # 引入数据库模型总量计数方法

from blog.models import Post , Category, Tag  # 引入post模型，Category模型，Tag模型


register = template.Library()  # 创建注册模板库实例


# 功能：模板标签——获取最新的几篇文章（最新文章）
# 实现方式：将get_recent_posts装饰为simple_tag
# 使用：在模板中添加{% get_recent_posts %}
@register.simple_tag
def get_recent_posts(num=5):
    return Post.objects.all()[:num]


# 功能：模板标签——返回文章的归档时间（归档）
# 使用：{% archives %}
@register.simple_tag
def archives():
    return Post.objects.dates('created_time', 'month', order='DESC')


# 功能：模板标签——获取所有现有文章分类（分类（文章数））
# 使用：{% get_categories %}
@register.simple_tag
def get_categories():
    # 顶部引用Category模型
    return Category.objects.annotate(num_posts=Count('post')).filter(num_posts__gt=0)


# 功能：模板标签——获取所有现有标签（标签云）
# 使用：{% get_tags %}
@register.simple_tag
def get_tags():
    return Tag.objects.annotate(num_posts=Count('post')).filter(num_posts__gt=0)
