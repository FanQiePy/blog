# -*- coding: utf-8 -*-
from django.shortcuts import render

# Create your views here.


def mycrawl(request):
    return render(request, 'crawl.html')
