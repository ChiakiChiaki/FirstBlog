from django.shortcuts import render,get_object_or_404
from django.http import  HttpResponse
from .models import Post,Category,Tag
from comments.form import CommentForm
from django.views import generic
from django.core.paginator import Paginator
from django.db.models import  Q



# Create your views here.

def index(request):
    post_list=Post.objects.all().order_by('-ctime')    #QuerySet  根据class meta 的ordering 也可以order_by指定

    return render(request, 'blog/index.html',context={'post_list':post_list})


def detail(request,post_id):


    post=get_object_or_404(Post,pk=post_id)

    views=post.add_views()
    Post.objects.filter(pk=post.pk).update(views=views)

    #缓存问题
    post=Post.objects.get(pk=post_id)


    form=CommentForm()
    comment_list=post.comment_set.all()
    context={'post': post,  'form': form, 'comment_list': comment_list}
    return render(request,'blog/detail.html',context=context)


def category(request,cate_id):
    cate=get_object_or_404(Category,pk=cate_id)
    post_list=Post.objects.filter(category_id__exact=cate.id).order_by('-ctime')

    return render(request, 'blog/index.html',context={'post_list':post_list})



#ctime.year->ctime__year
def archives(request,year,month):

    post_list=Post.objects.filter(ctime__year=year,ctime__month=month).order_by('-ctime')

    return render(request, 'blog/index.html', context={'post_list': post_list})


# 分别抽象“显示一个对象列表”和“显示一个特定类型对象的详细信息页面”这两种概念。

class IndexView(generic.ListView):
    model = Post
    template_name = 'blog/index.html'
    # ontext_object_name = 'post_list' #自动生成的就是这个名字
    paginate_by = 2



    def get_context_data(self,  **kwargs):

        context=super(IndexView, self).get_context_data(**kwargs)
        # 父类生成的字典中已有 paginator、page_obj、is_paginated  object_list/post_list模板变量

        paginator = context.get('paginator')
        page =  context.get('page_obj')
        is_paginated=context.get('is_paginated')

        page_data=self.page_data(paginator,page,is_paginated)

        if not page_data:
            page_data={}
        context.update(page_data)

        return context


    def page_data(self,paginator,page,is_paginated):

        if not is_paginated:
            return

        left=[]       #左边页码列表
        right=[]      #右边页码列表
        first=False  #第一页
        last=False   #最后一页
        left_has_more = False  #左边省略号
        right_has_more = False #右边省略号
        show_list_number=2
        page_range=paginator.page_range  #整个分页页码列表


        if page.number==1:

            #列表切片 右边超出范围只切列表末尾 不报错
            right=page_range[page.number-1+show_list_number-1 : page.number-1+show_list_number]

            if right[-1]<page_range[-1]-1:
                right_has_more=True
                last=True
            elif right[-1]<page_range[-1]:
                last = True

        elif page.number==page_range[-1]:
            page_begin=page.number-2
            left=page_range[page_begin if page_begin >=0 else 0:page.number-1]

            if left[0]>2:
                left_has_more = True
                first=True
            elif left[0]>1:
                first=True

        else:

            page_begin = page.number - 2
            left=page_range[page_begin if page_begin >=0 else 0:page.number-1]
            right=page_range[page.number-1+show_list_number-1 : page.number-1+show_list_number]


            if left[0] > 2:
                left_has_more = True
                first = True
            elif left[0] > 1:
                first = True


            if right[-1]<page_range[-1]-1:
                right_has_more=True
                last=True
            elif right[-1]<page_range[-1]:
                last = True

        data={
            'left':left,
            'right':right,
            'right_has_more':right_has_more,
            'left_has_more':left_has_more,
            'first':first,
            'last':last,
        }
        return data












class CategoryView(generic.ListView):
    model = Post
    template_name = 'blog/index.html'


    # context_object_name = 'post_list' #自动生成的就是这个名字

#listview有get_query_set方法
#从 URL 捕获的保存在实例的 kwargs args
    def get_queryset(self):
        cate=get_object_or_404(Category,pk=self.kwargs.get('cate_id'))
        return super(CategoryView,self).get_queryset().filter(category=cate)








class ArchivesView(generic.ListView):
    model = Post
    template_name = 'blog/index.html'
    # ontext_object_name = 'post_list' #自动生成的就是这个名字
    def get_queryset(self):
        return super(ArchivesView, self).get_queryset().filter(ctime__year=self.kwargs.get('year'),ctime__month=self.kwargs.get('month'))



class DetailView(generic.DetailView):
    model = Post
    template_name = 'blog/detail.html'
    context_object_name = 'post'

    def get(self, request, *args, **kwargs):
        response = super(DetailView, self).get(request, *args, **kwargs)

        views=self.object.add_views()
        Post.objects.filter(pk=self.object.pk).update(views=views)
        # 怎么在视图里解决？？？

        return response


    #self.object为获取的对象
    def get_context_data(self, **kwargs):
        context=super(DetailView,self).get_context_data(**kwargs)
        form=CommentForm()
        comment_list=self.object.comment_set.all()
        #字典update
        context.update({'form':form,'comment_list':comment_list})
        return context


class TagView(generic.ListView):
    model = Post
    template_name = 'blog/index.html'

    def get_queryset(self):
        tag=get_object_or_404(Tag,pk=self.kwargs.get('tag_id'))
        return super(TagView, self).get_queryset().filter(tag__exact=tag)



def search(request):

    q=request.GET.get('q')
    error_msg=''

    #i不区分大小写
    if not q:
        error_msg="请输入关键词"
        return render(request, 'blog/index.html', {'error_msg': error_msg})

    post_list = Post.objects.filter(Q(title__icontains=q) | Q(body__icontains=q))

    return render(request, 'blog/index.html', {'post_list': post_list,'error_msg': error_msg})















