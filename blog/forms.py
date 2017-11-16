from django.forms import ModelForm, Textarea

from .models import Post, Comment


class CommentForm(ModelForm):

    class Meta:
        model = Comment
        fields = ['text']
        labels = {'text': '', }
        widgets = {'text': Textarea(attrs={'cols': 20, 'rows': 3}), }


class PostForm(ModelForm):

    class Meta:
        model = Post
        fields = ['title', 'tags', 'text']
        # labels = {'title': '', 'text': '', }
        widgets = {'text': Textarea(attrs={'cols': 20, 'rows': 5}), }
