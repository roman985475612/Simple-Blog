from django.conf.urls import url

from . import views

app_name = 'blog'

urlpatterns = [
    url('^$', views.PostListView.as_view(), name='index'),
    url('^most-commented/$', views.PostByCommentsListView.as_view(), name='most_commented'),
    url('^last-commented/$', views.PostByLastCommentListView.as_view(), name='last_commented'),
    url('^most-viewed/$', views.PostByViewsListView.as_view(), name='most_viewed'),
    url('^rating/$', views.PostByRatingListView.as_view(), name='rating'),
    url('^post/(?P<pk>\d+)/$', views.PostDetailView.as_view(), name='post_detail'),
    url('^post/(?P<pk>\d+)/like/$', views.PostLikeRedirectView.as_view(), name='post_like'),
    url('^post/(?P<pk>\d+)/dislike/$', views.PostDislikeRedirectView.as_view(), name='post_dislike'),
    url('^post/(?P<pk>\d+)/comment/add/$', views.CommentCreateView.as_view(), name='comment_add'),
    url('^post-add/$', views.PostCreateView.as_view(), name='post_add'),
    url('^post/(?P<pk>\d+)/edit/$', views.PostUpdateView.as_view(), name='post_edit'),
    url('^post/(?P<pk>\d+)/delete/$', views.PostDeleteView.as_view(), name='post_delete'),
    url('^tag/add/$', views.TagCreateView.as_view(), name='tag_add'),
    url('^tag/$', views.TagListView.as_view(), name='tags'),
    url('^tag/(?P<slug>[\w-]+)/$', views.PostByTagListView.as_view(), name='tag_detail'),
]
