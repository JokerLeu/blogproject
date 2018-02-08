"""
表单文件

创建者：jokerleu
"""
from django import forms  # 导入django的表单模块
from .models import Comment  # 导入评论模型


# 评论表单
class CommentForm(forms.ModelForm):  # 继承于模型表
    class Meta:  # forms的内部类，用于关联参数
        model = Comment  # 模型=评论模型
        fields = ['name', 'email', 'url', 'text']  # 字段：用户名，邮箱，个人主页，评论内容
