from django.db import models
from django.contrib.auth.models import User
from django.contrib import admin
from django.db.models import Count, Max
from django.utils import timezone
from django.contrib.auth.models import AbstractBaseUser



class User(AbstractBaseUser, models.Model):
    username = models.CharField(max_length=50) 
    email = models.EmailField(blank=True, null=True)
    first_name = models.CharField(max_length=64)
    last_name = models.CharField(max_length=64, null=True, blank=True)



class Seller(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.PROTECT)
    address = models.CharField(max_length=100, blank=True, null=True)

    



class Platform(models.Model):
    name = models.CharField(max_length=64)
    url  = models.URLField(max_length = 200)

    def max_item(self):

        order_item = OrderItem.objects.values('item').annotate(max_item=Max('item__platform')).order_by()


class Item(models.Model):
    name = models.CharField(max_length=64)
    price = models.IntegerField()
    description = models.TextField()
    seller = models.ForeignKey(Seller, on_delete=models.CASCADE)
    platform = models.ManyToManyField(Platform)
    stock = models.IntegerField(default=0)
    
class OrderItem(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    order_date = models.DateField()



    
admin.site.register(Platform)
admin.site.register(Seller)
admin.site.register(Item)
admin.site.register(OrderItem)
