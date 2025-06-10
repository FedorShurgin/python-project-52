from django import forms
from django.forms import ModelForm
from task_manager.users.models import UsersModels

class UserForms(ModelForm):
    name = forms.CharField(label='Имя')
    last_name = forms.CharField(label='Фамилия')
    nickname = forms.CharField(label='Имя пользователя')
    password = forms.CharField(label='Пароль')
    passwor2 = forms.CharField(label='Подтверждение пароля')
    
    class Meta:
        model = UsersModels
        fields = ['name', 'last_name', 'nickname', 'password', 'passwor2']