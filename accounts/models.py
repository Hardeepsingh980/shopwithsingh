from django.db import models
from django.contrib.auth.models import User
from shop.models import Product

class Address(models.Model):
    address_id = models.AutoField(primary_key=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    country = models.CharField(max_length=30, null=True, blank=True)
    state = models.CharField(max_length=30, null=True, blank=True)
    city = models.CharField(max_length=30, null=True, blank=True)
    pincode = models.CharField(max_length=10, null=True, blank=True)
    phone = models.CharField(max_length=15, null=True, blank=True)
    street_address = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return self.user.username


class Favourites(models.Model):
    favourites_id = models.AutoField(primary_key=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    products = models.ManyToManyField(Product, blank=True)

    def __str__(self):
        return self.user.username