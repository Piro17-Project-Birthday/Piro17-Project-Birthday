from django.db import models

class User(models.Model):
    birth_year = models.CharField(max_length=250)
    birth_day = models.CharField(max_length=250)
    
class Post(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name="sender", null=True)
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name="receiver", null=True)
    nickname = models.CharField(max_length=20)
    message = models.TextField()
    is_private = models.BooleanField(default=False)