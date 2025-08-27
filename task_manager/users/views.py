from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, ListView, UpdateView

from task_manager.mixins import SuccessMessageMixin
from task_manager.users.forms import CustomUserCreationForm


class BaseView(LoginRequiredMixin, UserPassesTestMixin, SuccessMessageMixin):
    model = User
    success_url = reverse_lazy('users:users')
    error_message = "У вас нет прав для изменения другого пользователя."
    
    def test_func(self):
        user = self.get_object()
        return self.request.user == user
    
    def handle_no_permission(self):
        messages.error(self.request, self.error_message)
        return redirect(self.success_url)


class SignUpView(SuccessMessageMixin, CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'users/create.html'
    success_message = "Пользователь успешно зарегистрирован!"


class UsersView(ListView):
    model = User
    template_name = 'users/users.html'
    context_object_name = 'users'


class UsersUpdateView(BaseView, UpdateView):
    form_class = CustomUserCreationForm
    template_name = 'users/update.html'
    context_object_name = 'user'
    success_url = reverse_lazy('users:users')
    success_message = "Пользователь успешно изменен"


class UsersDeleteView(BaseView, DeleteView):
    template_name = 'users/delete.html'
    context_object_name = 'user'
    success_url = reverse_lazy('users:users')
    success_message = "Пользователь успешно удален"
