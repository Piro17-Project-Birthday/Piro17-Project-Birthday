from django import forms
from .models import Message
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")


import django
django.setup()
from users.models import User


class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        exclude = ('sender', 'receiver','is_private', 'profile_img')

class LoginedMessageForm(forms.ModelForm):
    class Meta:
        model = Message
        exclude = ('sender', 'receiver', 'profile_img')
        
class BirthdayPageForm(forms.ModelForm):
    CAKE_CHOICES = [
        ("choco", "초코"),
        ("strawberry", "딸기"),
        ("carrot", "당근"),
    ]
    from datetime import datetime
    
    
    selected_cake = forms.ChoiceField(choices=CAKE_CHOICES, widget=forms.RadioSelect)
    birthday = forms.DateField(
        widget=forms.widgets.DateInput(attrs={'type': 'date'})
    )
    class Meta:
        model = User
        fields = ('nickname', 'birthday', 'selected_cake')

class EditMyPageForm(forms.ModelForm):
    CAKE_CHOICES = [
        ("choco", "초코"),
        ("strawberry", "딸기"),
        ("carrot", "당근"),
    ]
    selected_cake = forms.ChoiceField(choices=CAKE_CHOICES, widget=forms.RadioSelect)
    class Meta:
        model = User
        fields = ('nickname','selected_cake')