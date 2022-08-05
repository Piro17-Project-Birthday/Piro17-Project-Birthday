import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    email = models.EmailField(null=True)
    full_name = models.CharField(null=True,max_length=50)
    birthday = models.DateField(null=True)

    
	
