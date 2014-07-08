from django import forms
from jungleapp.models import Jungle, Post
from django.contrib.auth.models import User

class UserForm(forms.ModelForm):
  password = forms.CharField(widget=forms.PasswordInput())
  class Meta:
    model = User
    fields = ('username', 'password')

class JungleForm(forms.ModelForm):
  class Meta:
    model = Jungle
    fields = ('name',)

class PostForm(forms.ModelForm):
  class Meta:
    model = Post
    fields = ()