from django.db import models
from django.contrib.auth.models import AbstractUser

class Product(models.Model):
    name = models.CharField(max_length=50)
    price = models.IntegerField()

class User(AbstractUser):
    
    def __str__(self):
        return self.first_name
    

    

    
