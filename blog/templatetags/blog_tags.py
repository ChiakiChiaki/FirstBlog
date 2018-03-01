#Author:Sun Jian


from django import template
from ..models  import  Post,Category,Tag

from django.db.models import Count


register = template.Library()

@register.simple_tag
def get_recent_posts(num=5):
    return Post.objects.all().order_by('ctime')[:num]

@register.simple_tag
def get_category():

    #post数量大于0的category类
    # q=Category.objects.annotate(num_post=Count('post'))
    # q[0].num_post=1
    # num_post属性

    return Category.objects.annotate(num_post=Count('post')).filter(num_post__gt=0)


@register.simple_tag
def archives():
    return Post.objects.dates('ctime',"month",order='DESC')


@register.simple_tag
def get_tags():
    return  Tag.objects.annotate(num_posts=Count('post')).filter(num_posts__gt=0)






