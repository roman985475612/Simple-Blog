from django.contrib import admin
from django.utils.safestring import mark_safe

from .models import Post, Category, Comment, Tag


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    date_hierarchy = 'pub_date'

    def tags_list_as_string(self, obj):
        return ', '.join([tag.title for tag in obj.tags.all()])
    tags_list_as_string.short_description = 'Tags'

    list_display = ('title', 'author', 'category', 'pub_date', 'upd_date', 'tags_list_as_string', 'get_photo')
    list_filter = ('author', 'category', 'tags',)
    search_fields = ['title', 'text']
    prepopulated_fields = {'slug': ('title',)}
    readonly_fields = ('views', 'likes', 'dislikes', 'rating', 'comments')
    save_on_top = True
    save_as = True

    def get_photo(self, obj):
        if obj.photo:
            return mark_safe(f'<img src="{ obj.photo.url }" width="50">')
        else:
            return '-'

    get_photo.short_description = 'Фото'


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'title')
    list_display_links = ('id', 'title')
    search_fields = ('title',)
    prepopulated_fields = {'slug': ('title',)}


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    date_hierarchy = 'pub_date'
    list_display = ('post', 'author', 'pub_date',)
    list_filter = ('post', 'author',)
    search_fields = ['text']


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('title', 'color',)
    list_filter = ('color',)
    prepopulated_field = {'slug': ('title',)}
