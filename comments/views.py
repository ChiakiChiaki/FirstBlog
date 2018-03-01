from django.shortcuts import render,get_object_or_404,redirect
from .models import Comment
from blog.models import Post
from .form import CommentForm

#判断数据是否有效 有效就加入对应文章的外键中去 然后再由文章逆向取出所有关联的评论

def post_comment(request,post_id):

    post=get_object_or_404(Post,pk=post_id)
    if request.method=='POST':
        form=CommentForm(request.POST)
        if form.is_valid():

            comment=form.save(commit=False)
            comment.post_id=post.id
            comment.save()
            return redirect(post)

        else:
            #错误信息
            comment_list=post.comment_set.all()
            context={'post':post,'form':form,'comment_list':comment_list}
            return render(request, 'blog/detail.html', context=context)
    return redirect(post)





