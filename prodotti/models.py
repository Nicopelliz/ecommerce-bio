import random
import string
from django.conf import settings

from django.contrib.auth.models import User
from django.db import models
from django.utils.text import slugify


# funzione da usare dentro le  slug
def rand_slug():
    return ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(3))

class Product(models.Model):
    name = models.CharField(max_length=200)
    price = models.FloatField()
    discount_price = models.FloatField(blank=True, null=True)
    description = models.TextField()
    image = models.ImageField(null=True, blank=True)
    stock = models.IntegerField()
    is_bio = models.BooleanField(default=False)
    digital = models.BooleanField(default=False)
    slug = models.SlugField(max_length=200, unique=True, editable=False)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(rand_slug() + "-" + str(self.name))
        super(Product, self).save(*args, **kwargs)

    @property
    def imageURL(self):
        try:
            url = self.image.url
        except:
            url = ''
        return url


class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, auto_created=True, blank=True, null=True)

    def __str__(self):
        return self.user.username


class OrderItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    # order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True, blank=True)
    quantity = models.IntegerField(default=1)
    date_added = models.DateTimeField(auto_now_add=True, editable=True)
    ordered = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username + \
               ' ' + self.product.name + \
               ' ' + str(self.quantity)

    def get_total_item_price(self):
        return self.quantity * self.product.price

    def get_total_discount_item_price(self):
        return self.quantity * self.product.discount_price

    def get_amount_saved(self):
        return self.get_total_item_price() - self.get_total_discount_item_price()

    def get_final_price(self):
        if self.product.discount_price:
            return self.get_total_discount_item_price()
        else:
            return self.get_total_item_price()

    class Meta:
        ordering = ['user', '-date_added']


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    items = models.ManyToManyField(OrderItem)
    start_date = models.DateTimeField(auto_now_add=True, blank=True)
    ordered_date = models.DateTimeField(auto_now_add=True)
    ordered = models.BooleanField(default=False, null=True)
    transaction_id = models.CharField(max_length=200, null=True)
    shipping_address = models.ForeignKey(
        'ShippingAddress', 
        on_delete=models.SET_NULL, 
        blank=True, null=True)
    payment = models.ForeignKey(
        'Payment', 
        on_delete=models.SET_NULL, 
        blank=True, null=True)
    

    def __str__(self):
        return self.user.username

    class Meta:
        ordering = ['ordered', 'start_date']

    def get_total_price(self):
        total = 0
        for order_item in self.items.all():
            total += order_item.get_final_price()
        return total

    def get_total_quantity(self):
        total_quantity = 0
        for order_item in self.items.all():
            total_quantity += order_item.quantity
        return total_quantity


PAYMENT_OPTIONS = (
    ('S','Stripe'),
    ('P','PayPal')
)


class ShippingAddress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    # order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True, blank=True)
    indirizzo = models.CharField(max_length=200, null=True)
    citta = models.CharField(max_length=100, null=True)
    provincia = models.CharField(max_length=3, null=True)
    codice_postale = models.CharField(max_length=100, null=True)
    date_added = models.DateTimeField(auto_now_add=True)
    opzioni_di_pagamento = models.CharField(max_length=1, choices=PAYMENT_OPTIONS, blank=True, null=True)

    def __str__(self):
        return self.user.username


class Payment(models.Model):
    stripe_charge_id = models.CharField(max_length=50)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, blank=True, null=True)
    amount = models.FloatField()
    time_stamp_field = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username

