# models.py
from django.db import models
from django.core.exceptions import ValidationError
from django.utils import timezone
from behairvauth.models import User
import datetime 

class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True,blank=True,related_name="user_profile")
    date_of_birth = models.DateField(null=True, blank=True)
    GENDER_MALE = 0
    GENDER_FEMALE = 1
    GENDER_CHOICES = [(GENDER_MALE, 'Male'), (GENDER_FEMALE, 'Female')]
    gender = models.IntegerField(choices=GENDER_CHOICES, null=True, blank=True)
    number = models.IntegerField(null=True, blank=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True, default="profile_pics/to/default/no-profile-picture-3")
    bio = models.TextField(null=True, blank=True)
    address = models.CharField(max_length=200, null=True, blank=True)
    location_number = models.CharField(max_length=10, null=True, blank=True)
    city = models.CharField(max_length=200, null=True, blank=True)
    country = models.CharField(max_length=200, null=True, blank=True)
    zip_code = models.CharField(max_length=10, null=True, blank=True)


    def __str__(self):
        return f"{self.user.username}'s Profile"
    
class Listing(models.Model):
    category = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    title = models.CharField(max_length=200)
    description = models.TextField()


class Event(models.Model):
    title = models.CharField(max_length=200)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()

    def __str__(self):
        return self.title


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)

class Place(models.Model):
    location = models.CharField(max_length=100)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    

    def clean(self):
        # Example custom validation for location
        if 'invalid' in self.location:
            raise ValidationError("Location cannot contain 'invalid'")