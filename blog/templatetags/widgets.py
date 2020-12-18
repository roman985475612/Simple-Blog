from django import template

from ..models import Category
from ..models import Post

register = template.Library()

@register.inclusion_tag('blog/widgets/category_widget.html')
def category_widget():
    return {'categories': Category.objects.all()}

@register.inclusion_tag('blog/widgets/popular_posts_widget.html')
def popular_posts_widget():
    return {'popular_posts': Post.objects.get_popular()}

@register.inclusion_tag('blog/widgets/recent_posts_widget.html')
def recent_posts_widget():
    return {'recent_posts': Post.objects.get_recent()}
