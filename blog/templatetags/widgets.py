from django import template

from ..models import Category
from ..models import Post

register = template.Library()

@register.inclusion_tag('blog/widgets/category_widget.html')
def category_widget():
    categories = Category.objects.all()
    return {'categories': categories}

@register.inclusion_tag('blog/widgets/popular_posts_widget.html')
def popular_posts_widget():
    popular_posts = Post.objects.get_popular()
    return {'popular_posts': popular_posts}
