from django import forms
from .models import TmiMessage



class TmiMessageForm(forms.ModelForm):
    class Meta:
        model = TmiMessage
        fields = ('content',)