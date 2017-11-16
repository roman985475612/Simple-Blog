from django.conf.urls import url

from . import views

app_name = 'blog'

urlpatterns = [
    url('^$', views.PostListView.as_view(), name='index'),
    url('^post/(?P<pk>\d+)/$', views.PostDetailView.as_view(), name='post_detail'),
    url('^post/(?P<pk>\d+)/comment-add/$',
        views.CommentCreateView.as_view(), name='comment_add'),
    url('^post-add/$', views.PostCreateView.as_view(), name='post_add'),
]
