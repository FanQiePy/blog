# -*- coding: utf-8 -*-
from django.urls import path

from .views import mycrawl

urlpatterns = [
    path('', mycrawl, name='mycrawl'),
]
