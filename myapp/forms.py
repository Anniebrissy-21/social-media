from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

from myapp.models import UserProfile,Posts,Stories,Comments

class LoginForm(forms.Form):
    username=forms.CharField(widget=forms.TextInput(attrs={"class":"form-control mt-2 shadow-none"}))
    password=forms.CharField(widget=forms.PasswordInput(attrs={"class":"form-control mt-2 shadow-none"}))

class RegisterForm(UserCreationForm):
    class Meta:
        model=User
        fields=["first_name","last_name","username","email","password1","password2"]


class ProfileForm(forms.ModelForm):
    class Meta:
        model=UserProfile
        fields=["bio","dob","phone","profile_picture"]

        widgets={
            "dob":forms.DateInput()
        }
        

class PostForm(forms.ModelForm):
    class Meta:
        model=Posts
        fields=["title","post_image","description"]
        

class StoryForm(forms.ModelForm):
    class Meta:
        model=Stories
        fields=["title","picture"]
        
class CommentForm(forms.ModelForm):
    class Meta:
        model=Comments
        fields=["text"]
        