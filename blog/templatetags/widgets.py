from django import template

from ..models import Category

register = template.Library()

@register.inclusion_tag('blog/widgets/category_widget.html')
def category_widget():
    categories = Category.objects.all()
    return {'categories': categories}
