"""
评论的视图文件
"""
from django.shortcuts import render, get_object_or_404, redirect  # 引入渲染，获取目标模型，重定向

from blog.models import Post  # 引入blog的文章模型
from .models import Comment  # 引入评论模型

from .forms import CommentForm # 引入评论表单


# 文章评论页面
def post_comment(request, post_pk):
    post = get_object_or_404(Post, pk=post_pk)  # 获取pk对应的文章模型实例
    if request.method == 'POST':
        form = CommentForm(request.POST)  # request.POST是个类字典对象
        # 如果提交的form符合表单格式要求
        if form.is_valid():
            # 利用表单生成模型实例，但先不保存到数据库中
            comment = form.save(commit=False)
            # 关联评论和提交的被评论的文章，外键post
            comment.post = post
            # 合并保存
            comment.save()
            # 重定向到post所在模型的get_absolute_url方法返回的url
            return redirect(post)
        # 表单有错误
        else:
            # 获取该文章的全部评论列表
            # post.comment_set.all()等价于Comment.objects.filter(post=post)
            comment_list = post.comment_set.all()
            context = {'post': post,  # 指定的文章
                       'form': form,  # 表单
                       'comment_list': comment_list # 全部评论列表
                       }
            return render(request, 'blog/detail.html', context=context)
    # 非POST请求，返回指定文章详情
    return redirect(post)
