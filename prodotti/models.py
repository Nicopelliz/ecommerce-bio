from django.db import models


class Product(models.Model):
    name = models.CharField(max_length=100)
    price = models.FloatField()
    stock = models.IntegerField(default=None)
    discount_price = models.FloatField(blank=True, null=True)
    description = models.TextField()
    objects = None
    image = models.CharField(max_length=2083, default=None)





