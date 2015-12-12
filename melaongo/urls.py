from django.conf.urls import url
from . import views

urlpatterns = [
    #url(r'^$', views.post_list, name='post_list'),
    url(r'^blog/$', views.post_list, name='post_list'),
    url(r'^blog/post/(?P<pk>[0-9]+)/$', views.post_detail, name='post_detail'),
    url(r'^blog/post/new/$', views.post_new, name='post_new'),
    url(r'^blog/post/(?P<pk>[0-9]+)/edit/$', views.post_edit, name='post_edit'),
    url(r'^blog/drafts/$', views.post_draft_list, name='post_draft_list'),
    url(r'^blog/post/(?P<pk>[0-9]+)/publish/$', views.post_publish, name='post_publish'),
    url(r'^blog/post/(?P<pk>[0-9]+)/remove/$', views.post_remove, name='post_remove'),
    url(r'^blog/post/(?P<pk>[0-9]+)/comment/$', views.add_comment_to_post, name='add_comment_to_post'),
    url(r'^blog/comment/(?P<pk>[0-9]+)/approve/$', views.comment_approve, name='comment_approve'),
    url(r'^blog/comment/(?P<pk>[0-9]+)/remove/$', views.comment_remove, name='comment_remove'),
    url(r'^blog/about/$',views.blog_about, name='blog_about'),
    #url(r'^blog/',views.blog),
    #url(r'^blog/post/(?P<pk>[0-9]+)/$', views.blog_post_detail, name='blog_post_detail'),
]
