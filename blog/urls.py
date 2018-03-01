#Author:Sun Jian

from django.conf.urls import url
from . import views


app_name='blog'
#detailView希望获取pk

urlpatterns = [
  url(r'^$',views.IndexView.as_view(),name='index'),

  url(r'^post/(?P<pk>[0-9]+)/$',views.DetailView.as_view(),name='detail'),

  url(r'^category/(?P<cate_id>[0-9]+)/$',views.CategoryView.as_view(),name='category'),

  url(r'archives/(?P<year>[0-9]{4})/(?P<month>[0-9]{1,2})/$',views.ArchivesView.as_view(),name='archives'),

  url(r'^tag/(?P<tag_id>[0-9]+)/$',views.TagView.as_view(),name='tag'),


  # url(r'^search/$',views.search ,name='search'),

]