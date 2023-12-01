# forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm,UserChangeForm
from blog.models import CustomUser

class CustomUserCreationForm(UserCreationForm):

    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'password1', 'password2', 'phone', 'first_name', 'last_name', 'gender', 'dob', 'designation', 'address', 'pincode', 'city', 'state', 'country', 'img')
        
class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = CustomUser
        fields = ('username', 'email','first_name', 'last_name', 'gender', 'dob', 'designation', 'address', 'pincode', 'city', 'state', 'country', 'img')

