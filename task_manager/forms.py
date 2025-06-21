from django.contrib.auth.views import LoginView
from django import forms
from django.contrib.auth.models import User


class CustomLoginView(LoginView):
    username = forms.CharField(label='Имя пользователя', initial='Имя пользователя',)
    password = forms.CharField(label='Пароль')

    class Meta:
        model = User
        fields = ('username', 'password')  