# -*- coding: utf-8 -*-
from django.shortcuts import render
from rest_framework import viewsets
from rest_framework import filters
from rest_framework.pagination import PageNumberPagination

from .serializers import HouseSerializer
from .models import House5i5j, ArticlePush
from .tasks import article_push
# Create your views here.


class GoodsPagination(PageNumberPagination):
    page_size = 25
    page_size_query_param = 'page_size'
    page_query_param = "page"
    max_page_size = 100


def mycrawl(request):
    return render(request, 'crawl.html')


class HouseViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = House5i5j.objects.all().order_by('id')
    serializer_class = HouseSerializer
    pagination_class = GoodsPagination

    filter_backends = (filters.SearchFilter, filters.OrderingFilter)
    search_fields = ('address', )
    ordering_fields = ('square', 'price', 'square_price')


def article_push_view(request):
    # article_push.apply_async()
    articles = ArticlePush.objects.all().order_by('-id')[:10]
    context = {'articles': articles}
    return render(request, 'crawl.html', context=context)
