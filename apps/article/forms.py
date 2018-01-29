# -*- coding: utf-8 -*-

from django.forms import ModelForm

from .models import Article, Comment


class ArticleForm(ModelForm):
    class Meta:
        model = Article
        fields = ['title', 'image', 'content', 'category']


class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ['username', 'email', 'content']