from datetime import datetime

from django.contrib.auth.models import User
from django.db import models
from django.template.defaultfilters import slugify
from django.urls import reverse


class Post(models.Model):
    title = models.CharField(max_length=200, unique=True)
    pub_date = models.DateTimeField('publication date', auto_now_add=True)
    upd_date = models.DateTimeField('update date', auto_now=True)
    text = models.TextField()
    comments = models.PositiveSmallIntegerField(default=0)
    last_comment_date = models.DateTimeField(default=datetime(1,1,1,0,0))
    views = models.PositiveIntegerField(default=0)
    likes = models.PositiveSmallIntegerField(default=0)
    dislikes = models.PositiveSmallIntegerField(default=0)
    rating = models.SmallIntegerField(default=0)
    author = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    tags = models.ManyToManyField('Tag')

    class Meta:
        db_table = 'posts'

    def get_absolute_url(self):
        return reverse('blog:post_detail', kwargs={'pk': self.id})

    def save(self, *args, **kwargs):
        self.rating = self.likes - self.dislikes
        super().save(*args, **kwargs)

    def __str__(self):
        return '{} by {}'.format(self.title[:15], self.author)


class Comment(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    pub_date = models.DateTimeField('publication date', auto_now_add=True)
    text = models.TextField()
    post = models.ForeignKey(Post, on_delete=models.CASCADE)

    class Meta:
        db_table = 'comments'
        ordering = ['-pub_date']

    def get_absolute_url(self):
        return reverse('blog:post_detail', kwargs={'pk': self.post.id})

    def __str__(self):
        return '{} by {}'.format(self.text[:15], self.author)


class Tag(models.Model):
    DEFAULT = 'default'
    PRIMARY = 'primary'
    SUCCESS = 'success'
    INFO = 'info'
    WARNING = 'warning'
    DANGER = 'danger'
    TAG_COLOR_CHOICES = (
        (DEFAULT, 'White'),
        (PRIMARY, 'Blue'),
        (SUCCESS, 'Green'),
        (INFO, 'Light blue'),
        (WARNING, 'Yellow'),
        (DANGER, 'Red')
    )
    color = models.CharField(max_length=10,
                             choices=TAG_COLOR_CHOICES,
                             default=DEFAULT)
    title = models.CharField(max_length=20, unique=True)
    slug = models.SlugField(unique=True, blank=True)

    class Meta:
        db_table = 'tags'
        ordering = ['title']

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return '{}'.format(self.title)


class View(models.Model):
    remote_addr = models.CharField(max_length=20)
    date_viewed = models.DateField(auto_now_add=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)

    class Meta:
        db_table = 'views'

    def __str__(self):
        return '{} on {} from {}'.format(self.post, self.remote_addr, self.date_viewed)


class Button(models.Model):
    is_liked = models.BooleanField()
    is_disliked = models.BooleanField()
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        db_table = 'buttons'

    def __str__(self):
        return '{} to {}'.format(self.user, self.post.title[:15])