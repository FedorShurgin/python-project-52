from django import forms
from django.contrib.auth.forms import UserCreationForm
from task_manager.users.models import UsersModels

class UserForms(UserCreationForm):
    first_name = forms.CharField(label='Имя')
    last_name = forms.CharField(label='Фамилия')
    username = forms.CharField(label='Имя пользователя')
    password1 = forms.CharField(label='Пароль')
    password2 = forms.CharField(label='Подтверждение пароля')
    
    class Meta:
        model = UsersModels
        fields = ['first_name', 'last_name', 'username', 'password1', 'password2']