from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm
from django.views.generic.edit import FormView
from django.shortcuts import render
from django.urls import reverse_lazy


class RegisterFormView(FormView):
    template_name = 'accounts/register.html'
    form_class = UserCreationForm
    success_url = reverse_lazy('blog:index')

    def form_valid(self, form):
        new_user = form.save()
        username = new_user.username
        password = form.cleaned_data['password1']
        user = authenticate(username=username, password=password)
        login(self.request, user)
        return super().form_valid(form)