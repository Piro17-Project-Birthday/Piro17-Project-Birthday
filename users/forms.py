from django import forms 
from django.contrib.auth.forms import UserCreationForm

from users.models import User

class LoginForm(forms.Form):
    username = forms.CharField(label='username')
    password = forms.CharField(widget=forms.PasswordInput,label='password')

    def clean(self):
        username = self.cleaned_data.get("username")
        password = self.cleaned_data.get("password")
        

        try:
            user = User.objects.get(username=username)

            if user.check_password(password):
                return self.cleaned_data
            else:
                print('err')
                raise forms.ValidationError("password is wrong")

        except User.DoesNotExist:
            raise forms.ValidationError("There is no user")

class SignupForm(UserCreationForm):
    
    class Meta:
        model = User
        fields = ['username',  'password1', 'password2','birthday']
    def save(self, user):
        user.save()
        
