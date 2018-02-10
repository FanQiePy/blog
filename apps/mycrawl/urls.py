# -*- coding: utf-8 -*-
from django.urls import path
from rest_framework import routers

from .views import mycrawl, HouseViewSet

router = routers.DefaultRouter()
router.register(r'house', HouseViewSet)

urlpatterns = [
    path('', mycrawl, name='mycrawl'),
]
