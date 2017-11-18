from django.conf.urls import url

from . import views

app_name = 'blog'

urlpatterns = [
    url('^$', views.PostListView.as_view(), name='index'),
    url('^post/(?P<pk>\d+)/$', views.PostDetailView.as_view(), name='post_detail'),
    url('^post/(?P<pk>\d+)/comment-add/$',
        views.CommentCreateView.as_view(), name='comment_add'),
    url('^post-add/$', views.PostCreateView.as_view(), name='post_add'),
    url('^post/(?P<pk>\d+)/edit/$', views.PostUpdateView.as_view(),
        name='post_edit'),
    url('^post/(?P<pk>\d+)/delete/$', views.PostDeleteView.as_view(),
        name='post_delete'),
    url('^tag-add/$', views.TagCreateView.as_view(), name='tag_add'),
]
