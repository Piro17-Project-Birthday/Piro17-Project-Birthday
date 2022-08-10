from django import forms
from django.contrib.auth.forms import UserCreationForm

from users.models import User

class LoginForm(forms.Form):
    username = forms.CharField(label='username')
    password = forms.CharField(widget=forms.PasswordInput,label='password')

    def clean(self):
        username = self.cleaned_data.get("username")
        password = self.cleaned_data.get("password")

        # 이 부분 로그인 폼 데이터 밸리데이션 하는 부분인데,
        # 유저 확인을 진행하고, LoginView에서도 유저 확인을 이중으로 진행합니다.
        # 로그인 폼을 다른데에서 사용하지 않는 것을 보아, 이중으로 로직이 돌아가는 것으로 보입니다.
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
