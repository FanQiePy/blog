# -*- coding: utf-8 -*-
import json
from django.http.response import HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_protect

from .models import Article, Category, ArticleFiled, Comment, Tag
from .forms import CommentForm


def index(request):
    articles = Article.objects.all().order_by('-time')

    # 根据文章归档日期和分类显示文章列表
    filed_date = request.GET.get('filed_date', '')
    category = request.GET.get('category', '')
    if filed_date and category:
        articles = Article.objects.filter(filed__date=filed_date).filter(category__name=category)
    elif filed_date:
        articles = Article.objects.filter(filed__date=filed_date)
    elif category:
        articles = Article.objects.filter(category__name=category)

    hot_articles = Article.objects.all().order_by('-click_num')
    article_filed = ArticleFiled.objects.all()
    categories = Category.objects.all()
    comments = Comment.objects.all().order_by("-time")
    context = {
        'articles': articles,
        'hot_articles': hot_articles,
        'categories': categories,
        'article_filed': article_filed,
        'comments': comments,
        'filed_date': filed_date,
        'category': category,
    }
    return render(request, 'index.html', context)


@csrf_protect
def detail(request, article_num=1229):
    try:
        article = Article.objects.get(article_num=article_num)
    except Article.DoesNotExist:
        return render(request, '404.html')
    if request.method == 'GET':
        tags = Tag.objects.filter(article=article)
        comments = Comment.objects.filter(article_id=article.id)
        comments_count = 0
        if comments.exists():
            comments_count = comments.count()
        context = {
            "article": article,
            "tags": tags,
            "comments_count":comments_count,
            "comments": comments,
        }
        return render(request, 'details.html', context)
    elif request.method == "POST":
        comment = Comment(article_id=article.id)
        form = CommentForm(data=request.POST, instance=comment)
        if form.is_valid():
            form.save(commit=True)
            data = {"status": "succeed"}
        else:
            errors = form.errors
            error_message = {}
            for key in errors:
                error_message[key] = errors[key][0]
            data = {"status": "failed", "error": error_message}
        return HttpResponse(json.dumps(data), content_type="application/json")
