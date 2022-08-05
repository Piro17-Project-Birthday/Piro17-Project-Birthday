from django.db import models

class Post(models.Model):
    nickname = models.CharField(max_length=20)
    message = models.TextField()
    is_private = models.BooleanField(default=False)
