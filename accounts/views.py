from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.mixins import UserPassesTestMixin
from django.contrib.auth.models import User
from django.views.generic import FormView, RedirectView, TemplateView
from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse


from .forms import UserForm


class RegisterFormView(FormView):
    template_name = 'accounts/register.html'
    form_class = UserCreationForm
    success_url = reverse_lazy('accounts:profile')

    def form_valid(self, form):
        new_user = form.save()
        username = new_user.username
        password = form.cleaned_data['password1']
        user = authenticate(username=username, password=password)
        login(self.request, user)
        return super().form_valid(form)


class UserUpdate(TemplateView):
    template_name = 'accounts/user_form.html'
    form_class = UserForm

    def get(self, request, *args, **kwargs):
        form = self.form_class(instance=self.request.user)
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(instance=self.request.user, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('accounts:profile')

        return render(request, self.tempalte_name, {'form': form})


class UserDelete(RedirectView):
    pattern_name = 'blog:index'

    def post(self, request, *args, **kwargs):
        request.user.delete()
        return super().post(request, *args, **kwargs)

