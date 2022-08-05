import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    desc = models.CharField(max_length=25, null=True, blank=True)
    #birth_date = models.DateField(verbose_name='생년월일')
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
