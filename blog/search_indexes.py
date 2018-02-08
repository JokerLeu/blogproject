"""
haystark全文索引文件

用法：要相对某个 app 下的数据进行全文检索，就要在该 app 下创建一个 search_indexes.py 文件
    然后创建一个 XXIndex 类（XX 为含有被检索数据的模型，如这里的 Post）
    并且继承 SearchIndex 和 Indexable。

创建者：jokerleu
修改时间：2018年2月3日
"""
from haystack import indexes  # 引用haystack索引

from .models import Post  # 引入文章模型


class PostIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)  # 约定内容命名为text

    # 获取模型——文章
    def get_model(self):
        return Post

    def index_queryset(self, using=None):
        return self.get_model().objects.all()  # 返回所有文章
