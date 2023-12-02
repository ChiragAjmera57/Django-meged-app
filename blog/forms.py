from django import forms

from .models import Comment, Post, Reply
from django import forms
from blog.models import CustomUser
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
