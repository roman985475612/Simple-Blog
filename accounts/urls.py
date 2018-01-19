from django.contrib.auth import views as auth_views
from django.urls import path

from .views import (
    PasswordChangeView,
    RegisterFormView,
    UserProfileView,
    UserPostsView,
    UserUpdateView,
    UserDeleteView,
    )

app_name = 'accounts'

urlpatterns = [
    path('login/', auth_views.login, {'template_name': 'accounts/login.html'}, name='login'),
    path('logout/', auth_views.logout, {'next_page': '/'}, name='logout'),
    path('register/', RegisterFormView.as_view(), name='register'),
    path('profile/', UserProfileView.as_view(), name='profile'),
    path('profile/change-password/', PasswordChangeView.as_view(), name='change_password'),
    path('profile/update/', UserUpdateView.as_view(), name='update'),
    path('profile/delete/', UserDeleteView.as_view(), name='delete'),
    path('posts/', UserPostsView.as_view(), name='posts'),
]
