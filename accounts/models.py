from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    
    address= models.CharField(max_length=60)
    address2= models.CharField(max_length=60)
    city= models.CharField(max_length=60)
    state= models.CharField(max_length=60)
    zop_number= models.CharField(max_length=10)

    def __str__(self):
        return self.user.username