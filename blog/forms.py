from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from ckeditor.widgets import CKEditorWidget

from .models import *



class BulkPostUploadForm(forms.Form):
    excel_file = forms.FileField()

class ReadOnlyAudioPlayerWidget(forms.Widget):
    def render(self, name, value, attrs=None, renderer=None):
        if value:
            return mark_safe('<audio controls src="{}"></audio>'.format(value.url))
        return "No audio file"
    
class PostForm(forms.ModelForm):
    text = forms.CharField(widget=CKEditorWidget())
    audio_file = forms.FileField(widget=ReadOnlyAudioPlayerWidget(), required=False)
    class Meta:
        model = Post
        fields = ('title', 'text','post_cat','tags','image','feature_img')

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment   
        fields = ('name', 'body')      
        
class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'password1', 'password2', )
        
        
class CustomUserChangeForm(UserChangeForm):
    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields =("email", "phone", "first_name", "last_name", "gender", "dob", "designation", "address", "pincode", "city", "state", "country", "img","preferred_language")
        widgets = {
            'dob': forms.DateInput(attrs={'type': 'date'}),
        }