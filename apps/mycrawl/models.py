from PIL import Image
from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.conf import settings

from article.models import change_image_size


# Create your models here.


class House5i5j(models.Model):
    city = models.CharField(max_length=15)
    area = models.CharField(max_length=30)
    house_type = models.CharField(max_length=15)
    layout = models.CharField(max_length=15)
    square = models.DecimalField(decimal_places=2, max_digits=6)
    price = models.IntegerField()
    date = models.DateField()
    address = models.CharField(max_length=25)
    house_url = models.URLField()
    square_price = models.DecimalField(decimal_places=1, max_digits=5)

    def __repr__(self):
        return self.house_url


def article_image_path(instance, filename):
    file_format = filename.split('.', 1)[1]
    return 'image/{}.{}'.format(instance.id, file_format)


class ArticlePush(models.Model):
    title = models.CharField(max_length=50)
    href = models.URLField()
    summary = models.CharField(max_length=200)
    time = models.DateField(auto_now=True)
    favour = models.CharField(max_length=10)
    image = models.ImageField(upload_to=article_image_path, null=True, blank=True)

    def __init__(self, *args, **kwargs):
        super(ArticlePush, self).__init__(*args, **kwargs)
        self.__original_image = self.image

    def check_image(self):
        return self.image != self.__original_image

    def __repr__(self):
        return self.title


@receiver(post_save, sender=ArticlePush)
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

