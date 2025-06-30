from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User


class CustomUserCreationForm(UserCreationForm):
    first_name = forms.CharField(label='Имя')
    last_name = forms.CharField(label='Фамилия')
    username = forms.CharField(
        label='Имя пользователя',
        help_text='Обязательное поле. Не более 150 символов. Только буквы, цифры и символы @/./+/-/_.'
        )
    password1 = forms.CharField(
        label='Пароль',
        help_text='Ваш пароль должен содержать как минимум 3 символа.'
        )
    password2 = forms.CharField(
        label='Подтверждение пароля',
        )

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username','password1', 'password2')
