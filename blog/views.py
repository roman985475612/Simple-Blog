from datetime import datetime

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
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

from .models import Post, Comment, Tag, View, Button
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
            )

        return self.posts.order_by('-upd_date')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['query'] = self.query
        context['title'] = 'Home'
        return context


class PostByTagListView(ListView):
    template_name = 'blog/post_list.html'
    context_object_name = 'post_list'

    def get_queryset(self):
        self.tag = get_object_or_404(Tag, slug=self.kwargs['slug'])
        self.post_list = self.tag.post_set.all()
        return self.post_list

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Posts'
        return context


class PostByCommentsListView(ListView):
    queryset = Post.objects.order_by('-comments')[:10]
    template_name = 'blog/post_list.html'
    context_object_name = 'post_list'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Posts'
        return context


class PostByLastCommentListView(ListView):
    queryset = Post.objects.order_by('-last_comment_date')[:10]
    template_name = 'blog/post_list.html'
    context_object_name = 'post_list'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Posts'
        return context


class PostByViewsListView(ListView):
    queryset = Post.objects.order_by('-views')[:10]
    template_name = 'blog/post_list.html'
    context_object_name = 'post_list'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Posts'
        return context


class PostByRatingListView(ListView):
    queryset = Post.objects.order_by('-rating')[:10]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Posts'
        return context
    

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
        context['title'] = self.get_object().title
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
        else:
            if obj.is_liked and not obj.is_disliked:
                obj.is_liked = False
                post.likes = F('likes') - 1
            
            elif not obj.is_liked and not obj.is_disliked:
                obj.is_liked = True
                post.likes = F('likes') + 1

            elif not obj.is_liked and obj.is_disliked:
                obj.is_liked = True
                post.likes = F('likes') + 1
                obj.is_disliked = False
                post.dislikes = F('dislikes') - 1

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
        else:
            if obj.is_liked and not obj.is_disliked:
                obj.is_liked = False
                post.likes = F('likes') - 1
                obj.is_disliked = True
                post.dislikes = F('dislikes') + 1

            elif not obj.is_liked and not obj.is_disliked:
                obj.is_disliked = True
                post.dislikes = F('dislikes') + 1

            elif not obj.is_liked and obj.is_disliked:
                obj.is_disliked = False
                post.dislikes = F('dislikes') - 1
        
        obj.save()
        post.save()
        return super().get_redirect_url(*args, **kwargs)


class CommentCreateView(LoginRequiredMixin, CreateView):
    model = Comment
    form_class = CommentForm

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


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    success_url = reverse_lazy('accounts:posts')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Add Post'
        return context

    def form_valid(self, form):
        form.instance.author = self.request.user
        messages.success(self.request, 'Post created.')
        return super().form_valid(form)


class PostUpdateView(UserPassesTestMixin, UpdateView):
    model = Post
    form_class = PostForm
    success_url = reverse_lazy('accounts:posts')

    def test_func(self):
        post_to_update = get_object_or_404(Post, pk=self.kwargs['pk'])
        return self.request.user == post_to_update.author
        
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Update Post'
        return context
        
    def form_valid(self, form):
        messages.success(self.request, 'Post updated.')
        return super().form_valid(form)


class PostDeleteView(UserPassesTestMixin, RedirectView):

    def get_queryset(self):
        return get_object_or_404(Post, pk=self.kwargs['pk'])

    def test_func(self):
        return self.request.user == self.get_queryset().author
    
    def post(self, request, *args, **kwargs):
        self.get_queryset().delete()
        messages.success(request, 'Post deleted.')
        return super().post(request, *args, **kwargs)
    
    def get_redirect_url(self, *args, **kwargs):
        return reverse('accounts:posts')


class TagListView(ListView):
    model = Tag
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Tags'
        return context


class TagCreateView(LoginRequiredMixin, CreateView):
    model = Tag
    form_class = TagForm
    success_url = reverse_lazy('blog:tags')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Add Tag"
        return context
