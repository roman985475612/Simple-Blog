from django.urls import path

from . import views

app_name = 'blog'

urlpatterns = [
    path('', views.PostListView.as_view(), name='index'),
    path('most-commented/', views.PostByCommentsListView.as_view(), name='most_commented'),
    path('last-commented/', views.PostByLastCommentListView.as_view(), name='last_commented'),
    path('most-viewed/', views.PostByViewsListView.as_view(), name='most_viewed'),
    path('rating/', views.PostByRatingListView.as_view(), name='rating'),
    path('post/<int:pk>/', views.PostDetailView.as_view(), name='post_detail'),
    path('post/(<int:pk>)/like/', views.PostLikeRedirectView.as_view(), name='post_like'),
    path('post/(<int:pk>)/dislike/', views.PostDislikeRedirectView.as_view(), name='post_dislike'),
    path('post/(<int:pk>)/comment/add/', views.CommentCreateView.as_view(), name='comment_add'),
    path('post-add/', views.PostCreateView.as_view(), name='post_add'),
    path('post/(<int:pk>)/edit/', views.PostUpdateView.as_view(), name='post_edit'),
    path('post/(<int:pk>)/delete/', views.PostDeleteView.as_view(), name='post_delete'),
    path('tag/add/', views.TagCreateView.as_view(), name='tag_add'),
    path('tag/', views.TagListView.as_view(), name='tags'),
    path('tag/<slug:slug>/', views.PostByTagListView.as_view(), name='tag_detail'),
]
