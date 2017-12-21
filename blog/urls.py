from django.urls import path

from .views import (
    PostListView,
    PostByCommentsListView,
    PostByLastCommentListView,
    PostByViewsListView,
    PostByRatingListView,
    PostDetailView,
    PostLikeRedirectView,
    PostDislikeRedirectView,
    CommentCreateView,
    PostCreateView,
    PostUpdateView,
    PostDeleteView,
    TagCreateView,
    TagListView,
    PostByTagListView
    )

app_name = 'blog'

urlpatterns = [
    path('', PostListView.as_view(), name='index'),
    path('most-commented/', PostByCommentsListView.as_view(), name='most_commented'),
    path('last-commented/', PostByLastCommentListView.as_view(), name='last_commented'),
    path('most-viewed/', PostByViewsListView.as_view(), name='most_viewed'),
    path('rating/', PostByRatingListView.as_view(), name='rating'),
    path('post/<int:pk>/', PostDetailView.as_view(), name='post_detail'),
    path('post/<int:pk>/like/', PostLikeRedirectView.as_view(), name='post_like'),
    path('post/<int:pk>/dislike/', PostDislikeRedirectView.as_view(), name='post_dislike'),
    path('post/<int:pk>/comment/add/', CommentCreateView.as_view(), name='comment_add'),
    path('post-create/', PostCreateView.as_view(), name='post_create'),
    path('post/<int:pk>/update/', PostUpdateView.as_view(), name='post_update'),
    path('post/<int:pk>/delete/', PostDeleteView.as_view(), name='post_delete'),
    path('tag/add/', TagCreateView.as_view(), name='tag_add'),
    path('tag/', TagListView.as_view(), name='tags'),
    path('tag/<slug:slug>/', PostByTagListView.as_view(), name='tag_detail'),
]
