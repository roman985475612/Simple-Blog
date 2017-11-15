from django.conf.urls import url

from .views import PostListView, PostDetailView, CommentCreateView

app_name = 'blog'

urlpatterns = [
    url('^$', PostListView.as_view(), name='index'),
    url('^post/(?P<pk>\d+)/$', PostDetailView.as_view(), name='post_detail'),
    url('^post/(?P<pk>\d+)/comment-add/$', CommentCreateView.as_view(),name='comment_add'),
]
