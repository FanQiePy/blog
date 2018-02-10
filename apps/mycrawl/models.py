from django.db import models

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
