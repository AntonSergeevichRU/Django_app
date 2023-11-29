from django.contrib import admin
from .models import *

@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = 'id', 'title', 'content', 'pub_date'


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = 'id', 'name'


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = 'id', 'name'


@admin.register(Author)
class AutorAdmin(admin.ModelAdmin):
    list_display = 'id', 'name', 'bio'