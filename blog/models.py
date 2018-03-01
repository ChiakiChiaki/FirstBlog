from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.db.models import  F

# Create your models here.

# 标题
# 分类 作者 创建时间
# 摘要 blank=True     表单验证允许输入空值
# 标签
# 作者 django.contrib.auth的User
class Post(models.Model):

    title=models.CharField(max_length=80)

    ctime=models.DateTimeField()
    mtime=models.DateTimeField()
    body=models.TextField()
    excerpt=models.CharField(max_length=200,blank=True)
    category=models.ForeignKey('Category',on_delete=models.CASCADE)
    tag=models.ManyToManyField('Tag',blank=True)

    auther = models.ForeignKey(User,on_delete=models.CASCADE)

    views=models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.title

    class Meta:
        ordering=['-ctime']

        #redirect（对象实例）会调用这个方法
    def get_absolute_url(self):
        return reverse('blog:detail',kwargs={'pk':self.pk})

    def save(self,*args,**kwargs):
        if not self.excerpt:
            self.excerpt=self.body[:80]+ '...'
        super(Post,self).save(*args,**kwargs)


        # self.views=self.views+1
        #self.views=F('views')+1  使用F 避免竞争

    def add_views(self):

        return F('views')+1
        # self.views = self.views + 1
        # self.save(update_fields=['views'])




class Category(models.Model):
    name=models.CharField(max_length=40)

    def __str__(self):
        return self.name


class Tag(models.Model):
    name=models.CharField(max_length=40)

    def __str__(self):
        return self.name







