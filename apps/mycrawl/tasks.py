# -*- coding: utf-8 -*-
# Create your tasks here
from __future__ import absolute_import, unicode_literals
from .python_article import zhihu_zhuanlang, COLUMNS
from .models import ArticlePush
from celery import shared_task


@shared_task
def article_push():
    for column in COLUMNS:
        article = zhihu_zhuanlang(column[0])
        last_data = ArticlePush.objects.filter(href=article['href'])
        print('starting task zhihu')
        if last_data.exists():
            continue
        data = ArticlePush()
        data.href = article['href']
        data.time = article['time'].split('T', 1)[0]
        data.title = article['title']
        data.summary = article['summary']
        data.favour = article['favour']
        data.image = 'image/zhihu-{}.jpg'.format(column[2])
        data.save()
    return
