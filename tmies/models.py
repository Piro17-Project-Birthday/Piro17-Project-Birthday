from django.db import models
from posts.models import BirthdayPage
from users.models import User

class TmiPage(models.Model):
    tmi_origin = models.OneToOneField(BirthdayPage, on_delete=models.CASCADE, primary_key=True)
    year = models.IntegerField(null=True)
    state = models.CharField(null=True, max_length=20)
    
class TmiMessage(models.Model):
    writer = models.ForeignKey(User, on_delete=models.CASCADE, related_name="writer", null=True)
    receiver = models.ForeignKey(TmiPage, on_delete=models.CASCADE)
    content = models.TextField()
    like = models.IntegerField(default=0)
    like_state = models.BooleanField(default=False, verbose_name="게시글좋아요")
    