from django.db import models
from django.contrib.auth.models import User
from product.models import Product
from datetime import date
from django.contrib import admin


class UserProfile(models.Model):
    user = models.ForeignKey(User, unique=True)
    add_book = models.ManyToManyField(Product, blank=True, through='ViewingPermission', editable=True)
    def __str__(self):
        return self.user
        
class ViewingPermission(models.Model):
    BookKey =models.ForeignKey(Product)
    person = models.ForeignKey(UserProfile)

    def __str__(self):
        return self.BookKey


