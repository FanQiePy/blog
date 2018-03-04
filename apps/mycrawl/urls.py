# -*- coding: utf-8 -*-
from django.urls import path
from rest_framework import routers

from .views import mycrawl, HouseViewSet, article_push_view

router = routers.DefaultRouter()
router.register(r'house', HouseViewSet)

urlpatterns = [
    path('test', mycrawl, name='mycrawl'),
    path('', article_push_view, name='article_push'),
]
