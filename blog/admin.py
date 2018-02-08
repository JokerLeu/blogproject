from django.contrib import admin
from .models import Post, Category, Tag # admin中导入需要管理的模型


#
class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'created_time', 'modified_time', 'category', 'author']

# 注册模型
admin.site.register(Post)
admin.site.register(Category)
admin.site.register(Tag)
