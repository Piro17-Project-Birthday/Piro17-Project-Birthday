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
        exclude = ('sender', 'receiver',)
        
class BirthdayPageForm(forms.ModelForm):
    CAKE_CHOICES = [
        ("초코 케이크", "초코"),
        ("딸기 케이크", "딸기"),
        ("치즈 케이크", "치즈"),
    ]
    from datetime import datetime
    
    date_range = 100    
    this_year = datetime.now().year
    selected_cake = forms.ChoiceField(choices=CAKE_CHOICES, widget=forms.RadioSelect)
    birthday = forms.DateField(
        widget=forms.SelectDateWidget(years=range(this_year - date_range, this_year + date_range))
        )
    class Meta:
        model = User
        fields = ('full_name', 'birthday', 'selected_cake')

class EditMyPageForm(forms.ModelForm):
    CAKE_CHOICES = [
        ("초코 케이크", "초코"),
        ("딸기 케이크", "딸기"),
        ("치즈 케이크", "치즈"),
    ]
    selected_cake = forms.ChoiceField(choices=CAKE_CHOICES, widget=forms.RadioSelect)
    class Meta:
        model = User
        fields = ('full_name','selected_cake')