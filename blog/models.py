from django.db import models


class Post(models.Model):
    title = models.CharField(max_length=200, unique=True)
    author = models.CharField(max_length=50)
    pub_date = models.DateTimeField('publication date', auto_now_add=True)
    upd_date = models.DateTimeField('update date', auto_now=True)
    text = models.TextField()
    tags = models.ManyToManyField('Tag')

    class Meta:
        db_table = 'posts'
        ordering = ['-pub_date']

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
    title = models.CharField(max_length=20)

    class Meta:
        db_table = 'tags'
        ordering = ['title']

    def __str__(self):
        return '{}'.format(self.title)
