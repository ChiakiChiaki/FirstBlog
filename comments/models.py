from django.db import models


# Create your models here.

class Comment(models.Model):


    name=models.CharField(max_length=30)
    email=models.EmailField(max_length=101)
    url=models.URLField(blank=True)
    text=models.TextField()
    #auto_now 每次保存 auto_now_add 第一次创建
    ctime=models.DateTimeField(auto_now_add=True)

    post = models.ForeignKey('blog.Post', on_delete=models.CASCADE)

    def __str__(self):
        return self.text[:20]




