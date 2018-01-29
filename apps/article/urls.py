# -*- coding: utf-8 -*-

from django.contrib import admin
from django.urls import path, re_path

from .views import detail

urlpatterns = [
    re_path('(?P<article_num>[1-9][0-9]{3})', detail, name='detail'),
]