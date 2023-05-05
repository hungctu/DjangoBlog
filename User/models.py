from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class customer_user(AbstractUser):
    fullname = models.CharField(max_length=100,null=False)
    user_image = models.ImageField(upload_to='images/')


