import markdown  # 引入markdown

from django.db import models
from django.contrib.auth.models import User  # 导入auth模型的user模型
from django.urls import reverse  # 反向解析url
from django.utils.html import strip_tags  # 引入去掉HTML标签的方法


# 分类名表，，可以从中选择，也可用户创建
class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):  # 防止查看时出现<QuerySet [<Category: Category object>]>
        return self.name  # 返回的是name名，更加直观


# 标签表，可以从中选择，也可用户创建
class Tag(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


# 文章表，帖子
class Post(models.Model):
    title = models.CharField(max_length=70)  # 标题
    body = models.TextField()  # 正文
    created_time = models.DateTimeField()  # 创建时间
    modified_time = models.DateTimeField()  # 最后修改时间
    excerpt = models.CharField(max_length=200, blank=True)  # 摘要，允许空
    category = models.ForeignKey(Category, on_delete=models.CASCADE)  # 分类名，外键
    tags = models.ManyToManyField(Tag, blank=True)  # 标签，外键
    author = models.ForeignKey(User, on_delete=models.CASCADE)  # 作者，外键
    views = models.PositiveIntegerField(default=0)  # 阅读量

    def __str__(self):
        return self.title

    # 获取url方法
    def get_absolute_url(self):
        return reverse('blog:detail', kwargs={'pk': self.pk})  # blog应用下的detail

    # 变换类，用于排列文章的顺序
    class Meta:
        # 指定排序方式为按时间倒序排列
        # 这样就不用再views里添加.order_by('-created_time')代码了
        ordering = ['-created_time']

    # 阅读量+1
    def increase_views(self):
        self.views += 1
        self.save(update_fields=['views'])

    # 复写保存方法
    def save(self, *args, **kwargs):
        # 如果文章没有摘要
        if not self.excerpt:
            # 实例化markdown备用
            md = markdown.Markdown(extensions=[
                'markdown.extensions.extra',
                'markdown.extensions.codehilite',
            ])
            # 摘掉文章被markdown渲染成的HTML标签，截取54个字符作为摘要
            self.excerpt = strip_tags(md.convert(self.body))[:54]

        # 调用父类的save方法保存数据
        super(Post, self).save(*args, **kwargs)
