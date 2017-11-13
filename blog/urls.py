from django.conf.urls import url

from .views import PostListView

app_name = 'blog'

urlpatterns = [
    url('^$', PostListView.as_view(), name='index'),
]
