from decimal import Decimal
from django.conf import settings
from django.db import models
from datetime import datetime


from fabtrendapp.models import Product
from django.contrib.auth.models import User
# Create your models here.


class WishList(models.Model):
    user_id = models.IntegerField()
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='wishlist_product')

    
    def __str__(self):
        return str(self.product.id)
     
    def get_total_cost(self):
        total_cost = sum(item.get_cost() for item in self.items.all())
        return total_cost - total_cost * (self.discount / Decimal('100'))
    
    def get_total_price(self):
        return sum(Decimal(item['price']) * item['quantity'] for item in self.cart.values())