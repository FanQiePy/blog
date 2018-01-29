# -*- coding: utf-8 -*-
from django.urls import path

from .views import myself

urlpatterns = [
    path('', myself, name='myself'),
]
