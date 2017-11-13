from django.test import TestCase

from blog.models import Post, Comment, Tag


class PostTestCase(TestCase):
    
    def setUp(self):
        Post.objects.create(
            title='Header',
            author='John Smith',
            text='This is a new text message!'
        )

    def test_post(self):
        post1 = Post.objects.get(title='Header')
        self.assertEqual(post1.author, 'John Smith')
        self.assertEqual(post1.text, 'This is a new text message!')

    def test_comment(self):
        post1 = Post.objects.get(pk=1)
        Comment.objects.create(
            post=post1,
            author='Joe Dow',
            text='This is a comment'
        )
        comment1 = Comment.objects.get(pk=1)
        self.assertEqual(comment1.author, 'Joe Dow')
        self.assertEqual(comment1.text, 'This is a comment')
