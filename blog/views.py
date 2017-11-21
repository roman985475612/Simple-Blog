from django.db.models import Q
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse, reverse_lazy

from .models import Post, Comment, Tag, View
from .forms import CommentForm, PostForm, TagForm


class PostListView(ListView):

    template_name = 'blog/post_list.html'
    context_object_name = 'post_list'

    def get_queryset(self):
        self.posts = Post.objects.all()
        self.query = self.request.GET.get('q')
        if self.query:
            self.posts = self.posts.filter(
                Q(title__icontains=self.query) |
                Q(text__icontains=self.query)
            ).order_by('-upd_date')

        return self.posts

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['query'] = self.query
        return context


class PostByTagListView(ListView):

    template_name = 'blog/post_list.html'
    context_object_name = 'post_list'

    def get_queryset(self):
        self.tag = get_object_or_404(Tag, slug=self.kwargs['slug'])
        self.post_list = self.tag.post_set.all()
        return self.post_list


class PostByCommentsListView(ListView):
    queryset = Post.objects.order_by('-comments')[:10]
    template_name = 'blog/post_list.html'
    context_object_name = 'post_list'


class PostByLastCommentListView(ListView):
    queryset = Post.objects.order_by('-last_comment_date')[:10]
    template_name = 'blog/post_list.html'
    context_object_name = 'post_list'


class PostByViewsListView(ListView):
    queryset = Post.objects.order_by('-views')[:10]
    template_name = 'blog/post_list.html'
    context_object_name = 'post_list'


class PostDetailView(DetailView):
    model = Post
    context_object_name = 'post'
    form_class = CommentForm

    def get_object(self):
        object = super().get_object()
        created = View.objects.get_or_create(
            post=object,
            remote_addr=self.request.META['REMOTE_ADDR']
        )[1]
        if created:
            object.views += 1
            object.save()

        return object

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
        self.post.comments += 1
        self.post.save()
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
