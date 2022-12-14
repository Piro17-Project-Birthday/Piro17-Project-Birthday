import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone

class User(AbstractUser):
    nickname = models.CharField(null=True, blank=True, max_length=50)
    email = models.EmailField(null=True, blank=True)
    birthday = models.DateField(null=True, blank=True,default=timezone.now)
    selected_cake = models.CharField(max_length=10, null=True, blank=True)

    
	
