import markdown
from markdown.extensions.toc import TocExtension  # 文章目录锚点用的模块1

from django.db.models import Q  # 引用数据库模型搜索模块
from django.views.generic import ListView, DetailView  # 引用django的类视图，表，内容
from django.utils.text import slugify  # 文章目录锚点用的模块2，用于处理中文标题
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse

from .models import Post, Category, Tag  # 引入帖子模型，文章分类模型
from comments.forms import CommentForm # 引入评论表单模型


# 首页——获取全部文章列表渲染——新类
class IndexView(ListView):
    model = Post  # 获取的模型是post
    template_name = 'blog/index.html'  # 用来渲染的模板
    context_object_name = 'post_list'  # 上下文的模型实例，即post的实例
    paginate_by = 10  # 设置分页每页文章数量

    # 覆写get_content_data方法，显示文章，表单，评论
    def get_context_data(self, **kwargs):
        # 首先获得父类生成的传递给模板的字典。
        context = super().get_context_data(**kwargs)
        # 取值
        paginator = context.get('paginator')
        page = context.get('page_obj')
        is_paginated = context.get('is_paginated')
        # 给分页导航条赋值
        pagination_data = self.pagination_data(paginator, page, is_paginated)
        # 分页导航条内容更新
        context.update(pagination_data)
        # 返回分页内容
        return context

#    # 覆写get_content_data方法，显示文章，表单，评论——旧
#    def get_context_data(self, **kwargs):
#        context = super(PostDetailView, self).get_context_data(**kwargs)
#        form = CommentForm()
#        comment_list = self.object.comment_set.all()
#        context.update({
#            'form': form,  # 表单
#            'comment_list': comment_list  # 评论列表
#        })
#        return context

    # 分页导航条 如：1 ... 34 35 36 ... 99
    def pagination_data(self, paginator, page, is_paginated):
        # 分页标记为空，则不分页
        if not is_paginated:
            return {}

        # 初始化数据
        # 第1页后及尾页前是否显示省略号
        left_has_more = False
        right_has_more = False
        # 是否显示首尾页号，就一页不显示页码
        first = False
        last = False
        # 当前页码
        page_number = page.number
        # 当前页码左右边的连续页码号
        left = []
        right = []
        # 分页后的总页数
        total_pages = paginator.num_pages
        # 分页页码表，如：[1, 2, 3, 4]
        page_range = paginator.page_range

        # 如果请求的页码为第一页
        if page_number == 1:
            # 添加后两页 1 2 3
            right = page_range[page_number:page_number + 2]  # 后两页
            # 如果后两页页码不是最后一页的前一页
            if right[-1] < total_pages -1:
                # 添加省略号 1 2 3 ...
                right_has_more = True
            # 如果后两页页码不是最后一页
            if right[-1] < total_pages:
                # 添加最后一页 1 2 3 ... 9
                last = True

        # 如果请求的页码为最后一页
        elif page_number == total_pages:
            # 添加前两页
            left = page_range[(page_number - 3) if (page_number - 3) > 0 else 0:page_number -1]
            # 如果最左边页码大于2
            if left[0] > 2:
                # 添加省略号 ... 3 4 5
                left_has_more = True
            # 如果最左边页码大于1
            if left[0] >1:
                # 添加第一页
                first = True

        else:
            # 确定首尾页
            left = page_range[(page_number - 3) if (page_number - 3) > 0 else 0:page_number - 1]
            right = page_range[page_number:page_number + 2]  # 后两页
            # 确定右边结构
            if right[-1] < total_pages - 1:
                right_has_more = True
            if right[-1] < total_pages:
                last = True
            # 确定左边结构
            if left[0] > 2:
                left_has_more = True
            if left[0] >1:
                first = True

        # 数据打包成字典
        data = {
            'left': left,
            'right': right,
            'left_has_more': left_has_more,
            'right_has_more': right_has_more,
            'first': first,
            'last': last,
        }

        return data

# 首页——获取全部文章列表渲染——旧方法
# def index(request):
#   post_list = Post.objects.all()  # 所有文章列表，倒叙排列
#   return render(request, 'blog/index.html', context={'post_list': post_list})


# 文章详情页面——获取特定ID（pk）的文章内容渲染——新
class PostDetailView(DetailView):
    model = Post  # 获取的模型是post
    template_name = 'blog/detail.html'  # 用来渲染的模板
    context_object_name = 'post'  # 上下文的模型实例，即post的实例

    # 覆写get方法，阅读量+1
    def get(self, request, *args, **kwargs):
        response = super().get(request, *args, **kwargs)
        # 阅读量+1
        # self.object是被访问的文章post
        self.object.increase_views()
        # 返回HttpRequest对象
        return response

    # 覆写get_object方法，渲染post的body——带markdown目录
    def get_object(self, queryset=None):
        post = super().get_object(queryset=None)
        md = markdown.Markdown(extensions=[
            'markdown.extensions.extra',
            'markdown.extensions.codehilite',
            # 'markdown.extensions.toc',
            TocExtension(slugify=slugify),  # 制作文章目录的锚点，这里非字符串，而是实例
        ])
        post.body = md.convert(post.body)
        post.toc = md.toc
        return post

#    # 覆写get_object方法，渲染post的body——无目录
#    def get_object(self, queryset=None):
#        post = super(PostDetailView, self).get_object(queryset=None)
#        post.body = markdown.markdown(post.body,
#                             extensions=[
#                                 'markdown.extensions.extra',
#                                 'markdown.extensions.codehilite',
#                                 'markdown.extensions.toc',
#                             ])
#        return post

    # 覆写get_content_data方法，显示文章，表单，评论
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        form = CommentForm()
        comment_list = self.object.comment_set.all()
        context.update({
            'form': form,  # 表单
            'comment_list': comment_list  # 评论列表
        })
        return context

# 文章详情页面——获取特定ID（pk）的文章内容渲染——旧
# def detail(request, pk):
#    post = get_object_or_404(Post, pk=pk)  # 根据文章id（即数据库表项的pk，private key）获取文章
#    # 阅读量+1
#    post.increase_views()
#    # 对文章内容进行markdown处理
#    post.body = markdown.markdown(post.body,
#                                  extensions=[
#                                      'markdown.extensions.extra',
#                                      'markdown.extensions.codehilite',
#                                      'markdown.extensions.toc',
#                                  ])
#    # 创建评论表单
#    form = CommentForm()
#    # 获取这篇post所关联的全部评论
#    comment_list = post.comment_set.all()
#    # 文章，评论表单，评论列表
#    context = {'post': post,
#               'form': form,
#               'comment_list': comment_list}
#    return render(request, 'blog/detail.html', context=context)


# 归档页面——获取特定年月（year，month）的文章列表渲染
# 由于网页格式与index相同，所以与index共用一个模板
class ArchivesView(ListView):
    model = Post
    template_name = 'blog/index.html'
    context_object_name = 'post_list'

    def get_queryset(self):
        year = self.kwargs.get('year')
        month = self.kwargs.get('month')
        return super(ArchivesView, self).get_queryset().filter(created_time__year=year,
                                                               created_time__month=month)
# 归档页面——获取特定年月（year，month）的文章列表渲染
# 由于网页格式与index相同，所以与index共用一个模板
# def archives(request, year, month):
#    post_list = Post.objects.filter(created_time__year=year,
#                                    created_time__month=month
#                                    )
#    return render(request, 'blog/index.html', context={'post_list': post_list})


# 分类页面——获取特定分类ID（category模型的pk）的文章列表渲染——新2
class CategoryView(ListView):  #也可直接继承IndexView
    model = Post
    template_name = 'blog/index.html'
    context_object_name = 'post_list'

    def get_queryset(self):
        cate = get_object_or_404(Category, pk=self.kwargs.get('pk'))
        return super().get_queryset().filter(category=cate)
# 分类页面——获取特定分类ID（category模型的pk）的文章列表渲染——新1
# class CategoryView(ListView):
#    model = Post  # 获取的模型是post
#    template_name = 'blog/index.html'  # 用来渲染的模板
#    context_object_name = 'post_list'  # 上下文的模型实例，即post的实例
#
#    def get_queryset(self):
#        cate = get_object_or_404(Category, pk=self.kwargs.get('pk'))
#        return super(CategoryView, self).get_queryset().filter(category=cate)
# 分类页面——获取特定分类ID（category模型的pk）的文章列表渲染——旧
#def category(request, pk):
#    cate = get_object_or_404(Category, pk=pk)  # 获取特定分类ID（pk）
#    post_list = Post.objects.filter(category=cate)
#    return render(request, 'blog/index.html', context={'post_list': post_list})


# 标签页面——获取特定标签下的文章列表
class TagView(ListView):  # 也可继承于IndexView，就不用设置变量
    model = Post
    template_name = 'blog/index.html'
    context_object_name = 'post_list'

    def fet_queryset(self):
        tag = get_object_or_404(Tag, pk=self.kwargs.get('pk'))
        return super().get_queryset().filter(tags=tag)


# # 搜索页面——获取搜索的文章列表——旧
# def search(request):
#    # 在请求中获取q表单
#    q = request.GET.get('q')
#    error_msg = ''
#    # 如果q中无内容
#    if not q:
#        error_msg = "请输入搜索内容"
#        return render(request, 'blog/index.html', {'error_msg': error_msg})
#    # q中有内容
#    post_list = Post.objects.filter(Q(title__icontains=q) | Q(body__icontains=q))
#    return render(request, 'blog/index.html', {'error_msg': error_msg,
#                                               'post_list': post_list})
