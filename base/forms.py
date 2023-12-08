from django.forms import ModelForm
from .models import Room, Message, User
# from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

from django import forms
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import get_user_model


class RoomForm(ModelForm):
    class Meta:
        model = Room
        fields = '__all__'
        exclude = ['host', 'participants']


class MessageForm(ModelForm):
    class Meta:
        model = Message
        fields = ['body']


class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ['avatar','name','username', 'email', 'bio']


class MyUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['name', 'username', 'email', 'password1', 'password2', 'avatar']


class ChangePasswordForm(forms.Form):
    new_password = forms.CharField(widget=forms.PasswordInput)
    def clean_new_password(self):
        new_password = self.cleaned_data.get('new_password')
        return new_password