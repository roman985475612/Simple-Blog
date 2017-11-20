from django.forms import ModelForm, Textarea

from .models import Post, Comment, Tag


class CommentForm(ModelForm):

    class Meta:
        model = Comment
        fields = ['text']
        labels = {'text': '', }
        widgets = {
            'text': Textarea(attrs={
                'cols': 20,
                'rows': 3,
                'placeholder': 'Add a public commint...'
            }),
        }


class PostForm(ModelForm):

    class Meta:
        model = Post
        fields = ['title', 'tags', 'text']
        widgets = {'text': Textarea(attrs={'cols': 20, 'rows': 5}), }


class TagForm(ModelForm):

    class Meta:
        model = Tag
        fields = ['title', 'color']
