from django.conf.urls import url

from .views import PostListView, PostDetailView

app_name = 'blog'

urlpatterns = [
    url('^$', PostListView.as_view(), name='index'),
    url('^post/(?P<pk>\d+)/$', PostDetailView.as_view(), name='post_detail'),
]
