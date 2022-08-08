from django import forms
from .models import Message
from users.models import User


class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        exclude = ('sender', 'receiver',)
        
class BirthdayPageForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('full_name', 'birthday')