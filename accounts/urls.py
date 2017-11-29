from django.conf.urls import url
from django.contrib.auth import views as auth_views

from . import views

app_name = 'accounts'

urlpatterns = [
    url('^login/$', auth_views.login, {'template_name': 'accounts/login.html'}, name='login'),
]