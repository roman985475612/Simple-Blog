from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse, reverse_lazy

from .models import Post, Comment, Tag
from .forms import CommentForm, PostForm, TagForm


class PostListView(ListView):
    model = Post


class PostDetailView(DetailView):
    model = Post
    context_object_name = 'post'
    form_class = CommentForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = self.form_class
        return context


class CommentCreateView(CreateView):
    model = Comment
    form_class = CommentForm

    def get_queryset(self):
        self.post = get_object_or_404(Post, pk=self.kwargs['pk'])
        return self.post

    def form_valid(self, form):
        form.instance.post = self.get_queryset()
        form.instance.author = 'John Smith'
        return super().form_valid(form)


class PostCreateView(CreateView):
    model = Post
    form_class = PostForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['header'] = 'Add new post'
        return context

    def form_valid(self, form):
        form.instance.author = 'John Smith'
        return super().form_valid(form)


class PostUpdateView(UpdateView):
    model = Post
    form_class = PostForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['header'] = 'Editing a post'
        return context


class PostDeleteView(DeleteView):
    model = Post
    success_url = reverse_lazy('blog:index')


class TagListView(ListView):
    model = Tag


class TagCreateView(CreateView):
    model = Tag
    form_class = TagForm
    success_url = reverse_lazy('blog:tags')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['header'] = "Adding tag"
        return context