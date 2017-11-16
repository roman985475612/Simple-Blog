from django.test import TestCase
from django.urls import reverse

from blog.models import Post


class PostListViewTest(TestCase):

    def test_post_list_view(self):
        response = self.client.get(reverse('blog:index'))
        self.assertEqual(response.status_code, 200)


class PostDetailViewTest(TestCase):

    def setUp(self):
        Post.objects.create(
            title='Header',
            author='John Smith',
            text='This is a new text message!'
        )
        
    def test_post_detail_view(self):
        post = Post.objects.get(title='Header')
        response = self.client.get(reverse('blog:post_detail', kwargs={'pk': post.id}))
        self.assertEqual(response.status_code, 200)


class PostCreateViewTest(TestCase):

    def test_post_create_view(self):
        response = self.client.get(reverse('blog:post_add'))
        self.assertEqual(response.status_code, 200)