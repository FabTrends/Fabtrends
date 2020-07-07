import os
import random
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.db import models
from django.db.models.signals import pre_save
from django.db.models import Q
from django.urls import reverse
from django.db.models.signals import post_save
User = settings.AUTH_USER_MODEL


AVAILABILITY_PRODUCT = (
    ('STOCK', 'In Stock'),
    ('OUT OF STOCK', 'Out Of Stock')
)


class contact(models.Model):
    name = models.CharField(max_length=500)
    phoneno = models.CharField(max_length=500)
    email= models.EmailField(max_length=500,blank=True, null=True)
    subject = models.CharField(max_length=500,blank=True, null=True)
    message = models.CharField(max_length=255)
    created_at =models.DateTimeField(auto_now_add=True,null=True)
    class Meta:
        db_table = "contact"

    def __str__(self):
        return self.name


class category(models.Model):
    name = models.CharField(max_length=500)

    class Meta:
        db_table = "category"

    def __str__(self):
        return self.name


class subcategory(models.Model):
    name = models.CharField(max_length=500)
    category = models.ForeignKey(category, on_delete=models.CASCADE, related_name='subcategory')
    image = models.ImageField(upload_to='images/', blank=True, null=True)

    class Meta:
        db_table = "subcategory"

    def __str__(self):
        return self.name


class Product(models.Model):
    id = models.AutoField(primary_key=True)
    productbrand = models.CharField(max_length=500, default='')
    name = models.CharField(max_length=500)
    published_on = models.DateField(auto_now=True)
    image = models.ImageField(upload_to='images/')
    image1 = models.ImageField(upload_to='images1/', blank=True, null=True)
    image2 = models.ImageField(upload_to='images1/', blank=True, null=True)
    image4 = models.ImageField(upload_to='images1/', blank=True, null=True)
    subcategory = models.ForeignKey(subcategory, on_delete=models.CASCADE)
    description = models.TextField(default='')
    material = models.CharField(max_length=500, default='')
    quantity = models.IntegerField(default=0)
    price = models.IntegerField(default=0)
    discounted_price = models.IntegerField(default=0)
    size = models.CharField(max_length=500, default='')
    Type = models.CharField(max_length=500, default='')
    Occasion = models.CharField(max_length=500, default='')
    pattern = models.CharField(max_length=500, default='')
    color = models.CharField(max_length=500, default='')
    Features = models.CharField(max_length=500, default='')
    productcode = models.CharField(max_length=500, default='')
    
    availabily = models.CharField(
        choices=AVAILABILITY_PRODUCT, max_length=20, blank=True, null=True)
    active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True,blank=True, null=True)
    updated = models.DateTimeField(auto_now=True,blank=True, null=True)
    TAG_CHOICES = (
        ('new', 'NEW'),
        ('stylish', 'STYLISH'),
        ('trending', 'TRENDING'),
        ('beautiful', 'BEAUTIFUL'),
        ('awesome', 'AWESOME'),
        ('popular', 'POPULAR'),
        ('swank', 'SWANK'),
        ('cool', 'COOL'),
        ('fashionable', 'FASHIONABLE'),
        ('snazzy', 'SNAZZY'),
        ('exculsive', 'EXCLUSIVE'),
        ('dashing', 'DASHING'),
    )
    tag = models.CharField(max_length=20, choices=TAG_CHOICES)

    class Meta:
        db_table = "product"

    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('fabtrendapp:productView', args=[self.id, self.name])



class FAQs(models.Model):
    question = models.TextField(max_length=500)
    answer = models.TextField()
    created_at =models.DateTimeField(auto_now_add=True,null=True)

    class Meta:
        db_table = "FAQs"

    def __str__(self):
        return self.question


class feedback(models.Model):
    experience = models.CharField(max_length=200)
    comments = models.CharField(max_length=200)
    name = models.CharField(max_length=200)
    phone = models.CharField(max_length=200)
    created_at =models.DateTimeField(auto_now_add=True,null=True,blank=True)
    class Meta:
        db_table = "feedback"

    def __str__(self):
        return self.name


class query(models.Model):
    name = models.CharField(max_length=200)
    phone = models.CharField(max_length=200)
    query = models.CharField(max_length=200)
    created_at =models.DateTimeField(auto_now_add=True,null=True,blank=True)
    class Meta:
        db_table = "query"

    def __str__(self):
        return self.name
