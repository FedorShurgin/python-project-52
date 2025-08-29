from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.views import LoginView
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView

from task_manager.mixins import SuccessMessageMixin, UniversalTemplateMixin
from task_manager.users.forms import CustomUserCreationForm


class SignUpView(
    UniversalTemplateMixin,
    SuccessMessageMixin,
    CreateView
):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('login')
    success_message = "Пользователь успешно зарегистрирован!"
    page_title = "Регистрация"
    submit_text = "Зарегистрировать"


class MyLoginView(SuccessMessageMixin, LoginView):
    template_name = 'login.html'
    success_message = "Вы залогинены"
    success_url = reverse_lazy('home')


def logout_user(request):
    logout(request)
    messages.success(request, "Вы разлогинены")
    return redirect('home')
