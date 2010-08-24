from django.db import models
from datetime import date
from django.contrib import admin


class PricingDate(models.Model):
    readableDate = models.CharField('Rental Period', max_length=200,editable=True)
    dateUntil= models.DateField(auto_now=False, auto_now_add=False,editable=True)
    price = models.FloatField('Price Displayed',editable=True)
    durationSLUG = models.SlugField("Slug Name", blank=False, help_text=("Used for parry up product and pricing"), max_length=255)
    
    def __str__(self):
        return self.durationSLUG
        
class PriceList(models.Model):
    name = models.CharField(max_length=128)
    add_price = models.ManyToManyField(PricingDate)
    
    def __str__(self):
        return self.name

