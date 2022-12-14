from django.db import models
from posts.models import BirthdayPage
from users.models import User

class PhotoPage(models.Model):
    photo_origin = models.OneToOneField(BirthdayPage, on_delete=models.CASCADE, primary_key=True)
    year = models.IntegerField(null=True)
    state = models.CharField(null=True, max_length=20)
    

class Photo(models.Model):
    photo_uploader = models.ForeignKey(User, on_delete=models.CASCADE, related_name="photo_uploader", null=True)
    receiver = models.ForeignKey(PhotoPage, on_delete=models.CASCADE)
    title = models.CharField(max_length=50, verbose_name="제목")
    req_photo = models.ImageField(upload_to='photos/%Y%m%d', verbose_name="사진")
