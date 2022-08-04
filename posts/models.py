from django.db import models

class Post(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name="sender", null=True)
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name="receiver")
    nickname = models.CharField(max_length=20)
    message = models.TextField()
    is_private = models.BooleanField(default=False)