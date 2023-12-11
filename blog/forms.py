from django import forms
from .models import *
from django import forms
from django.contrib.auth.forms import UserCreationForm,UserChangeForm


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title', 'text','post_cat','tags','image','feature_img')

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']

class ReplyForm(forms.ModelForm):
    class Meta:
        model = Reply
        fields = ['text']
        
        
class CustomUserCreationForm(UserCreationForm):

    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'password1', 'password2', )
        
class CustomUserChangeForm(UserChangeForm):

    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = UserCreationForm.Meta.fields + ("email", "phone", "first_name", "last_name", "gender", "dob", "designation", "address", "pincode", "city", "state", "country", "img")