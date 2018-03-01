#Author:Sun Jian
from haystack import indexes
from .models import Post

class PostIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)

    def get_model(self):  # 重载get_model方法，必须要有！
        return Post

    def index_queryset(self, using=None): #重载index_..函数

        return self.get_model().objects.all()