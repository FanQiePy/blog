# -*- coding: utf-8 -*-
import random
from PIL import Image
from datetime import datetime
from django.db import models
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from django.conf import settings
from ckeditor.fields import RichTextField

from bs4 import BeautifulSoup
from datetime import date
# Create your models here.


def article_image_path(instance, filename):
    return 'image/{}-{}'.format(instance.id, filename)


class Tag(models.Model):
    name = models.CharField(verbose_name='标签', max_length=20)

    def __repr__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(verbose_name='类名', max_length=20)
    count = models.IntegerField(verbose_name='文章数量', default=0)

    class Meta:
        verbose_name = '文章分类'
        verbose_name_plural = verbose_name

    def __repr__(self):
        return self.name


class ArticleFiled(models.Model):
    date = models.CharField(verbose_name='归档月份', max_length=10)

    class Meta:
        verbose_name = '文章归档'
        verbose_name_plural = verbose_name

    def __repr__(self):
        return self.date


def _make_article_filed():
    """按照年月份进行归档
    """
    filed_name = '{}年{}月'.format(date.today().strftime('%Y'), date.today().strftime('%m'))
    article_filed = ArticleFiled.objects.filter(date=filed_name)
    if not article_filed.exists():
        article_filed = ArticleFiled(date=filed_name)
        article_filed.save()
        return article_filed.id
    return article_filed[0].id


class Article(models.Model):
    __original_image = None
    __original_content = None

    @classmethod
    def _make_article_num(cls):
        """生成四位数的文章编号
        """
        retries = 10
        while True:
            num = random.randint(1001, 9999)
            article = cls.objects.filter(article_num=str(num))
            if article.exists():
                retries -= 1
                if retries > 0:
                    continue
                else:
                    print('it is impossible, LOL!!!')
            else:
                break
        return str(num)

    title = models.CharField(verbose_name='标题', max_length=50)
    image = models.ImageField(verbose_name='封面图片', null=True, blank=True,
                              upload_to=article_image_path)
    content = RichTextField(verbose_name='内容')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True, blank=True)
    click_num = models.IntegerField(verbose_name='点击数', default=0)
    like_num = models.IntegerField(verbose_name='点赞数', default=0)
    time = models.DateTimeField(verbose_name='发布时间', default=datetime.now)
    instruction = models.CharField(verbose_name='封面引文', max_length=200, null=True, blank=True)
    article_num = models.CharField(max_length=4, unique=True, verbose_name='文章编号', null=True, blank=True)
    filed = models.ForeignKey(ArticleFiled, on_delete=models.CASCADE, null=True, blank=True,
                              default=_make_article_filed, verbose_name='文章归档')
    tags = models.ManyToManyField(Tag, through='ArticleTag', through_fields=('article', 'tag'),
                                  verbose_name='文章标签')

    def __init__(self, *args, **kwargs):
        super(Article, self).__init__(*args, **kwargs)
        self.__original_content = self.content
        self.__original_image = self.image


    def check_image(self):
        return self.image != self.__original_image

    def check_content(self):
        return self.content != self.__original_content

    def set_ori_image(self):
        self.__original_image = self.image

    def set_ori_content(self):
        self.__original_content = self.content

    class Meta:
        verbose_name = u'文章'
        verbose_name_plural = verbose_name

    def __repr__(self):
        return self.title

    def save(self, *args, **kwargs):
        # tree = BeautifulSoup(self.content, 'lxml')
        # text = tree.get_text("", strip=True).encode('utf-8')
        # self.instruction = text.split("", maxsplit=200) + '...'
        if not self.article_num:
            self.article_num = self._make_article_num()
        super(Article, self).save(*args, **kwargs)


class ArticleTag(models.Model):
    article = models.ForeignKey('Article', on_delete=models.CASCADE)
    tag = models.ForeignKey('Tag', on_delete=models.CASCADE)


class Comment(models.Model):
    email = models.EmailField(verbose_name='邮件地址')
    username = models.CharField(verbose_name='用户名', max_length=16)
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    content = models.CharField(verbose_name='评论内容', max_length=72)
    time = models.DateTimeField(verbose_name='评论时间', default=datetime.now)

    class Meta:
        verbose_name = u'评论'
        verbose_name_plural = verbose_name

    def article_num(self):
        return self.article.article_num

    def __repr__(self):
        return self.username


def create_instruction(instance, *args, **kwargs):
    """生成文章在索引页的显示内容
    """
    if instance.check_content:
        tree = BeautifulSoup(instance.content, 'lxml')
        text = tree.get_text("", strip=True)
        if len(text) > 160:
            instance.instruction = text[:160] + '...'
        else:
            instance.instruction = text
        instance.set_ori_content()


pre_save.connect(create_instruction, sender=Article)


@receiver(post_save, sender=Article)
def change_image_size(instance, *args, **kwargs):
    """更改图片尺寸使其适合在索引页显示
    """
    if instance.check_image:
        image_f = Image.open(instance.image)
        out = image_f.resize((240, 135), Image.ANTIALIAS)
        with open(settings.MEDIA_ROOT+ '/'+ instance.image.name, 'wb') as f:
            out.save(f)
            f.close()
        instance.set_ori_image()



