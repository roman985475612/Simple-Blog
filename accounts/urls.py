from django.views.generic import TemplateView
from django.contrib.auth import views as auth_views
from django.urls import path

from .views import (
    PasswordChangeView,
    RegisterFormView,
    UserUpdate,
    UserDelete,
    )

app_name = 'accounts'

urlpatterns = [
    path('login/', auth_views.login, {'template_name': 'accounts/login.html'}, name='login'),
    path('logout/', auth_views.logout, {'next_page': '/'}, name='logout'),
    path('register/', RegisterFormView.as_view(), name='register'),
    path('profile/', TemplateView.as_view(template_name='accounts/profile.html'), name='profile'),
    path('profile/change-password/', PasswordChangeView.as_view(), name='change_password'),
    path('profile/delete/', UserDelete.as_view(), name='delete'),
    path('profile/update/', UserUpdate.as_view(), name='update'),
    path('posts/', TemplateView.as_view(template_name='accounts/user_posts.html'), name='posts'),
]
