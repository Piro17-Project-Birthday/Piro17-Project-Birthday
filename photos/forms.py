from django.forms import ModelForm
from .models import Photo

class PhotoCreateForm(ModelForm):
    class Meta:
        model = Photo
        fields = ['title', 'req_photo']