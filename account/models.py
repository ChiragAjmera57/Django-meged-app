from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
    )
    gender = models.CharField(max_length=60,null=True,choices=GENDER_CHOICES,blank=True)
    phone = models.PositiveBigIntegerField(null=True,blank=True)
    dob = models.DateField(null=True,blank=True)
    img = models.ImageField(null=True,blank=True)
    designation = models.CharField(max_length=50,null=True,blank=True)
    address = models.TextField(max_length=50,null=True,blank=True)
    pincode = models.PositiveIntegerField(null=True,blank=True)
    city = models.CharField(max_length=80,null=True,blank=True)
    state = models.CharField(max_length=90,null=True,blank=True)
    country = models.CharField(max_length=50,null=True,blank=True)
    
    
    # user_profile_img = models.ImageField(upload_to='profile')
   