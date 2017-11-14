from django.test import TestCase
from django.urls import reverse


class PostListViewTest(TestCase):

    def test_post_list_view(self):
        response = self.client.get(reverse('blog:index'))
        self.assertEqual(response.status_code, 200)
