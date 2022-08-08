from django.db import models
from users.models import User

class BirthdayPage(models.Model):
    owner = models.OneToOneField(User, on_delete=models.CASCADE)
    
class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name="sender", null=True)
    receiver = models.ForeignKey(BirthdayPage, on_delete=models.CASCADE)
    nickname = models.CharField(max_length=20)
    message = models.TextField()
    is_private = models.BooleanField(default=False)
    