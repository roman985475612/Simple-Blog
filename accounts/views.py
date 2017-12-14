from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.mixins import UserPassesTestMixin
from django.contrib.auth.models import User
from django.views.generic.edit import FormView, UpdateView, DeleteView
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy


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


class UserUpdateView(UserPassesTestMixin, UpdateView):
    model = User
    template_name = 'accounts/user_form.html'
    fields = ['first_name', 'last_name', 'email']
    success_url = reverse_lazy('accounts:profile')
    raise_exception = True

    def test_func(self):
        user = get_object_or_404(User, pk=self.kwargs['pk'])
        return self.request.user == user



class UserDeleteView(UserPassesTestMixin, DeleteView):
    model = User
    template_name = 'accounts/user_confirm_delete.html'
    success_url = reverse_lazy('blog:index')
    raise_exception = True

    def test_func(self):
        user = get_object_or_404(User, pk=self.kwargs['pk'])
        return self.request.user == user
