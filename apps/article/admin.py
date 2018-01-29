from django.contrib import admin

from .models import Article, ArticleFiled, Category, Comment
# Register your models here.


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):

    list_display = ('title', 'content', 'image', 'category')
    list_display_links = ('title', )
    list_filter = ('category', )
    list_select_related = True
    list_per_page = 30


@admin.register(ArticleFiled)
class ArticleFiledAdmin(admin.ModelAdmin):
    list_display = ('date', )
    list_display_links = ('date', )
    list_select_related = True
    list_per_page = 20


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'count')
    list_display_links = ('name', )
    list_select_related = True
    list_per_page = 20


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('email', 'username', 'article', 'content', 'time')
    list_display_links = ('username', )
    list_select_related = True
    list_per_page = 50
