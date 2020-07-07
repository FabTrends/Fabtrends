from decimal import Decimal
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator, RegexValidator
from django.db import models
from django.shortcuts import reverse
from django.utils.translation import gettext_lazy as _
from fabtrendapp.models import Product
from django.dispatch import receiver
from django.db.models.signals import post_save

ADDRESS_TYPE_CHOICES = (
    ('Home', 'Home'),
    ('Office', 'Office'),
    ('Other', 'Other')
)




class Order(models.Model):
    order_id = models.CharField(max_length=50,blank=True,null=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,blank=True,null=True)
#id = models.AutoField(primary_key=True, **options)
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Phone Number must be entered in the format: "
                                                                   "'+999999999'. Up to 15 digits allowed.")
    email_regex = RegexValidator(regex=r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$')
    username = models.CharField(max_length=100,blank=True,null=True)
    first_name = models.CharField(max_length=60)
    last_name = models.CharField(max_length=60)
    email = models.EmailField(_('e-mail'), validators=[email_regex], blank=False,null=True)
    phone_number = models.CharField(_('phone number'), validators=[phone_regex], max_length=17, blank=False,null=True)
    house_number= models.CharField(max_length=150,blank=True,null=True)
    
    town = models.CharField(max_length=150,blank=True,null=True)
    district = models.CharField(max_length=150,blank=True,null=True)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100,blank=True,null=True)
    country = models.CharField(default="India",max_length=50,blank=True,null=True,) 
    full_address = models.CharField(max_length=150)
    postal_code = models.CharField(max_length=30)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    delivered = models.BooleanField(default=False,blank=True)
    paid = models.BooleanField(default=True)
    refund_requested = models.BooleanField(default=False)
    returned = models.BooleanField(default=False)
    refund_granted = models.BooleanField(default=False)
    canceled = models.BooleanField(default=False)
    shipped = models.BooleanField(default=False)
    discount = models.IntegerField(default=0,
                                   validators=[MinValueValidator(0),
                                               MaxValueValidator(100)])
    address_type = models.CharField(choices=ADDRESS_TYPE_CHOICES, max_length=10, blank=True, null=True)
    ordered_date = models.DateTimeField(blank=True,null=True)
    ordered = models.BooleanField(default=False)
    shipped = models.BooleanField(default=False)
    out_for_delivery = models.BooleanField(default=False)
    
    
    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return 'Order {}'.format(self.id)

    def get_total_cost(self):
        total_cost = sum(item.get_cost() for item in self.items.all())
        return total_cost - total_cost * (self.discount / Decimal('100'))
   
   
class OrderItem(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,blank=True,null=True)
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, related_name='order_items', on_delete=models.CASCADE)
    price = models.IntegerField(default=0)
    quantity = models.PositiveIntegerField(default=1)
    created = models.DateTimeField(auto_now_add=True,blank=True, null=True)
    updated = models.DateTimeField(auto_now=True,blank=True, null=True)
    
    def __str__(self):
        return '{}'.format(self.id)

    def get_cost(self):
        return self.price * self.quantity
        
class Refund(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    reason = models.TextField()
    refund_accepted = models.BooleanField(default=False)
    email = models.EmailField()

    def __str__(self):
        return f"{self.pk}"
        
class CheckZipcode(models.Model):
    zipcode = models.CharField(max_length=10)

    def __str__(self):
        return self.zipcode