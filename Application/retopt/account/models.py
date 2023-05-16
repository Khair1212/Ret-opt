from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from PIL import Image
from django.conf import settings
# Create your models here.

class User(AbstractUser):
    is_customer=models.BooleanField(default=False)
    is_analyst=models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)

class Analyst(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE,blank=True, null=True)
    name = models.CharField(max_length=100)
    email = models.EmailField()
    DOB = models.DateField()
    gender_choices = (
            ('M', 'Male'),
            ('F', 'Female')
        )
    
    gender = models.CharField(max_length=1, choices=gender_choices)
    city_code = models.CharField(max_length=2)  

class Customer(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE,blank=True, null=True)
    name = models.CharField(max_length=100)
    email = models.EmailField()
    DOB = models.DateField()
    gender_choices = (
            ('M', 'Male'),
            ('F', 'Female')
        )
    
    gender = models.CharField(max_length=1, choices=gender_choices)
    city_code = models.CharField(max_length=2)


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')

    def __str__(self):
        return f'{self.user.username} Profile'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        img = Image.open(self.image.path)

        if img.height>300 or img.width>300:
            output_size = (300,300)
            img.thumbnail(output_size)
            img.save(self.image.path)