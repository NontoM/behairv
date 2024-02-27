from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
import datetime 



class User(AbstractUser):
    email = models.EmailField(max_length=254, unique=True)
    is_customer= models.BooleanField(default=False,blank=True,null=True)
    is_business = models.BooleanField(default=False,blank=True,null=True)
    is_stylist = models.BooleanField(default=False,blank=True,null=True)
    is_admin = models.BooleanField(default=False,blank=True,null=True)
    is_paid =models.BooleanField(default=False,blank=True,null=True)
    is_activation =models.BooleanField(default=False,blank=True,null=True)
    customerid =models.CharField(max_length=200,blank=True,null=True)
    number =  models.IntegerField(blank=True, null=True)
    address =models.CharField(max_length=200,blank=True,null=True)
    location_number = models.CharField(max_length=10, null=True, blank=True)
    country =models.CharField(max_length=200,blank=True,null=True)
    city =  models.CharField(max_length=200,blank=True,null=True)
    zip_code = models.CharField(max_length=10, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.username)
    
    class Meta(AbstractUser.Meta):
       swappable = 'AUTH_USER_MODEL'


