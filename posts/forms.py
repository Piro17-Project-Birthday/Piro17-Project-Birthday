from django import forms
from .models import Post
from users.models import User


class PostForm(forms.ModelForm):

    class Meta:
        model = Post
        # fields = '__all__'
        exclude = ('sender', 'receiver',)
        
class BirthdayPageForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ('full_name', 'birthday')