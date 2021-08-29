from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model, authenticate, login

User = get_user_model()

# from .models import CustomUser

#
# class CustomUserCreationForm(UserCreationForm):
#     class Meta(UserCreationForm):
#         model = CustomUser
#         fields = ['username', 'password1', 'password2', 'phone_number', 'email']


class SignUpForm(UserCreationForm):  # from medium.com example
    first_name = forms.CharField(max_length=30, required=True, help_text='', label='نام')

    class Meta:
        model = User
        fields = ('username', 'first_name', 'password1')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        del self.fields['password2']

# class VerifyForm(forms.ModelForm):
