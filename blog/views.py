from datetime import datetime

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import F, Q
from django.views.generic import (
    RedirectView,
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
    )
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse, reverse_lazy

from .models import Post, Category, Comment, Tag, View, Button
from .forms import CommentForm, PostForm, TagForm


class PostListView(ListView):
    template_name = 'blog/post_list.html'
    paginate_by = 2
    context_object_name = 'post_list'

    def get_queryset(self):
        self.posts = Post.objects.all()
        self.query = self.request.GET.get('q')
        if self.query:
            self.posts = self.posts.filter(
                Q(title__icontains=self.query) |
                Q(text__icontains=self.query)
            )

        return self.posts.order_by('-upd_date')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['query'] = self.query
        return context


class PostByCategory(ListView):
    template_name = 'blog/post_list_mini.html'
    context_object_name = 'post_list'
    paginate_by = 2

    def get_queryset(self):
        self.category = get_object_or_404(Category, slug=self.kwargs['slug'])
        self.post_list = self.category.posts.all();
        return self.post_list

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.category
        return context


class PostByTagListView(ListView):
    template_name = 'blog/post_grid.html'
    context_object_name = 'post_list'
    paginate_by = 2

    def get_queryset(self):
        self.tag = get_object_or_404(Tag, slug=self.kwargs['slug'])
        self.post_list = self.tag.post_set.all()
        return self.post_list

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.tag
        return context


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


class PostByRatingListView(ListView):
    queryset = Post.objects.order_by('-rating')[:10]


class PostDetailView(DetailView):
    model = Post
    context_object_name = 'post'
    form_class = CommentForm

    def get_object(self):
        obj = super().get_object()
        View.objects.get_or_create(
            post=obj,
            remote_addr=self.request.META['REMOTE_ADDR']
        )
        obj.refresh_from_db()
        return obj

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = self.form_class
        return context


class PostLikeRedirectView(LoginRequiredMixin, RedirectView):
    pattern_name = 'blog:post_detail'

    def get_redirect_url(self, *args, **kwargs):
        post = get_object_or_404(Post, pk=self.kwargs['pk'])
        user = self.request.user
        obj, created = Button.objects.get_or_create(post=post, user=user,
            defaults={'is_liked': True, 'is_disliked': False})
        
        if created:
            post.likes = F('likes') + 1
            messages.success(self.request, 'Added likes')
        else:
            if obj.is_liked and not obj.is_disliked:
                obj.is_liked = False
                post.likes = F('likes') - 1
                messages.success(self.request, 'Minus likes')
            
            elif not obj.is_liked and not obj.is_disliked:
                obj.is_liked = True
                post.likes = F('likes') + 1
                messages.success(self.request, 'Added likes')

            elif not obj.is_liked and obj.is_disliked:
                obj.is_liked = True
                post.likes = F('likes') + 1
                obj.is_disliked = False
                post.dislikes = F('dislikes') - 1
                messages.success(self.request, 'Added likes and minus dislike')

        obj.save()
        post.save()
        return super().get_redirect_url(*args, **kwargs)


class PostDislikeRedirectView(LoginRequiredMixin, RedirectView):
    pattern_name = 'blog:post_detail'

    def get_redirect_url(self, *args, **kwargs):
        post = get_object_or_404(Post, pk=self.kwargs['pk'])
        user = self.request.user
        obj, created = Button.objects.get_or_create(post=post, user=user,
            defaults={'is_liked': False, 'is_disliked': True})
        if created:
            post.dislikes = F('dislikes') + 1
            messages.success(self.request, 'Add dislike')
        else:
            if obj.is_liked and not obj.is_disliked:
                obj.is_liked = False
                post.likes = F('likes') - 1
                obj.is_disliked = True
                post.dislikes = F('dislikes') + 1
                messages.success(self.request, 'Add dislike and minus like')

            elif not obj.is_liked and not obj.is_disliked:
                obj.is_disliked = True
                post.dislikes = F('dislikes') + 1
                messages.success(self.request, 'Add dislike')

            elif not obj.is_liked and obj.is_disliked:
                obj.is_disliked = False
                post.dislikes = F('dislikes') - 1
                messages.success(self.request, 'Minus dislike')
        
        obj.save()
        post.save()
        return super().get_redirect_url(*args, **kwargs)


class CommentCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Comment
    form_class = CommentForm
    success_message = 'Comment created.'

    def get_queryset(self):
        self.post = get_object_or_404(Post, pk=self.kwargs['pk'])
        return self.post

    def form_valid(self, form):
        form.instance.post = self.get_queryset()
        form.instance.author = self.request.user
        self.post.comments += 1
        self.post.last_comment_date = datetime.now()
        self.post.save()
        return super().form_valid(form)


class PostCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name_suffix = '_create'
    success_url = reverse_lazy('accounts:posts')
    success_message = 'Post created'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class PostUpdateView(UserPassesTestMixin, SuccessMessageMixin, UpdateView):
    model = Post
    form_class = PostForm
    template_name_suffix = '_update'
    success_url = reverse_lazy('accounts:posts')
    success_message = 'Post updated'

    def test_func(self):
        post_to_update = get_object_or_404(Post, pk=self.kwargs['pk'])
        return self.request.user == post_to_update.author
        

class PostDeleteView(UserPassesTestMixin, RedirectView):

    def get_queryset(self):
        return get_object_or_404(Post, pk=self.kwargs['pk'])

    def test_func(self):
        return self.request.user == self.get_queryset().author
    
    def post(self, request, *args, **kwargs):
        self.get_queryset().delete()
        messages.success(request, 'Post deleted')
        return super().post(request, *args, **kwargs)
    
    def get_redirect_url(self, *args, **kwargs):
        return reverse('accounts:posts')
