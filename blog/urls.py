from django.urls import path

from .views import (
    PostListView,
    PostDetailView,
    PostCreateView,
    PostUpdateView,
    PostDeleteView,
    PostLikeRedirectView,
    PostDislikeRedirectView,
    CommentCreateView,
    PostByCategory,
    PostByTagListView
    )

app_name = 'blog'

urlpatterns = [
    path(''                             , PostListView.as_view()           , name='index'),
    path('post/add/'                    , PostCreateView.as_view()         , name='post_create'),
    path('post/<slug:slug>/'            , PostDetailView.as_view()         , name='post_detail'),
    path('post/<slug:slug>/update/'     , PostUpdateView.as_view()         , name='post_update'),
    path('post/<slug:slug>/delete/'     , PostDeleteView.as_view()         , name='post_delete'),
    path('post/<slug:slug>/like/'       , PostLikeRedirectView.as_view()   , name='post_like'),
    path('post/<slug:slug>/dislike/'    , PostDislikeRedirectView.as_view(), name='post_dislike'),
    path('post/<slug:slug>/comment/add/', CommentCreateView.as_view()      , name='comment_add'),
    path('category/<slug:slug>/'        , PostByCategory.as_view()         , name='category'),
    path('tag/<slug:slug>/'             , PostByTagListView.as_view()      , name='tag_detail'),
]
