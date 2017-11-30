from django.conf.urls import url
from django.contrib.auth import views as auth_views

from . import views

app_name = 'accounts'

urlpatterns = [
    url('^login/$', auth_views.login,
        {'template_name': 'accounts/login.html'}, name='login'),
    url('^logout/$', auth_views.logout,
        {'next_page': '/'}, name='logout'),
    url('^register/$', views.RegisterFormView.as_view(), name='register'),
]
