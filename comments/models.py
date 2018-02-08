from django.db import models


# Create your models here.
# 评论模型表
class Comment(models.Model):
    name = models.CharField(max_length=100)  # 用户名
    email = models.EmailField(max_length=255)  # 邮箱账号
    url = models.URLField(blank=True)  # 个人主页，可为空
    text = models.TextField()  # 评论内容
    created_time = models.DateTimeField(auto_now_add=True)  # 评论时间，自动创建

    post = models.ForeignKey('blog.Post', on_delete=models.CASCADE)  # 文章，外键blog的post表（默认为ID）

    def __str__(self):
        return self.text[:20]  # 返回评论的前20个字
