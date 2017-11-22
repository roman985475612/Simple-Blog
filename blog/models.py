from datetime import datetime

from django.db import models
from django.template.defaultfilters import slugify
from django.urls import reverse


class Post(models.Model):
    title = models.CharField(max_length=200, unique=True)
    author = models.CharField(max_length=50)
    pub_date = models.DateTimeField('publication date', auto_now_add=True)
    upd_date = models.DateTimeField('update date', auto_now=True)
    text = models.TextField()
    comments = models.PositiveSmallIntegerField(default=0)
    last_comment_date = models.DateTimeField(default=datetime(1,1,1,0,0))
    views = models.PositiveIntegerField(default=0)
    likes = models.PositiveSmallIntegerField(default=0)
    dislikes = models.PositiveSmallIntegerField(default=0)
    tags = models.ManyToManyField('Tag')

    class Meta:
        db_table = 'posts'
        ordering = ['-upd_date']

    def get_absolute_url(self):
        return reverse('blog:post_detail', kwargs={'pk': self.id})

    def __str__(self):
        return '{} by {}'.format(self.title[:15], self.author)


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    author = models.CharField(max_length=50)
    pub_date = models.DateTimeField('publication date', auto_now_add=True)
    text = models.TextField()

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
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    remote_addr = models.CharField(max_length=20)
    date_viewed = models.DateField(auto_now_add=True)

    class Meta:
        db_table = 'views'

    def __str__(self):
        return '{} on {} from {}'.format(self.post, self.remote_addr, self.date_viewed)
