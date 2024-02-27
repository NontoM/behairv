from django.db import models
from behairvauth.models import User
from datetime import datetime, time


class Service(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name="user_service")
    name = models.CharField(max_length=100,blank=True,null=True)
    description = models.TextField(max_length=100,blank=True,null=True)
    price = models.DecimalField(max_digits=10,default=0.00,decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class Appointment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True,blank=True,related_name="user_appointment")
    service = models.ForeignKey(Service, on_delete=models.CASCADE, null=True,blank=True,related_name="user_service_appointment")
    date = models.DateField(blank=True,null=True)
    time = models.TimeField(blank=True, null=True)
    note = models.TextField(max_length=100,blank=True,null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)



# models.py

class Working_hours(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name="user_working_hours")
    DAY_CHOICES = [
        ('Monday', 'Monday'),
        ('Tuesday', 'Tuesday'),
        ('Wednesday', 'Wednesday'),
        ('Thursday', 'Thursday'),
        ('Friday', 'Friday'),
        ('Saturday', 'Saturday'),
        ('Sunday', 'Sunday'),
    ]
    day = models.CharField(max_length=10, choices=DAY_CHOICES, blank=True, null=True)
    opening_time = models.TimeField(blank=True, null=True)
    closing_time = models.TimeField(blank=True, null=True)
    additional_info = models.TextField(max_length=100, blank=True, null=True)
    closed = models.BooleanField(default=False, null=True) # Field to represent if the business is closed on this day
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.user.username} - {self.day}'

    
class Catalog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True,blank=True,related_name="user_catalog")
    service = models.ForeignKey(Service, on_delete=models.CASCADE, null=True,blank=True,related_name="user_service_catalog")
    appointment = models.ForeignKey(Appointment, on_delete=models.CASCADE, null=True,blank=True,related_name="user_appointment_catalog")
    working_hours = models.ForeignKey(Working_hours, on_delete=models.CASCADE, null=True,blank=True,related_name="user_working_hours_catalog")
    business_name = models.CharField(max_length=100,blank=True,null=True)
    business_contact = models.CharField(max_length=100,blank=True,null=True)
    bio = models.TextField(blank=True,null=True)
    business_cover_pic = models.ImageField(upload_to='business_cover_pics/', blank=True, null=True, default="business_cover_pics/to/default/no-image.png")
    business_logo = models.ImageField(upload_to='business_logo/', blank=True, null=True, default="business_logo/to/default/no-profile-picture.png")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
