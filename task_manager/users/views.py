from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, ListView, UpdateView

from task_manager.users.forms import CustomUserCreationForm


class SignUpView(CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'users/create.html'
    
    def form_valid(self, form):
        messages.success(self.request, "Пользователь успешно зарегистрирован!")
        return super().form_valid(form)


class UsersView(ListView):
    model = User
    template_name = 'users/users.html'
    context_object_name = 'users'


class UsersUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = User
    form_class = CustomUserCreationForm
    template_name = 'users/update.html'
    context_object_name = 'user'
    success_url = reverse_lazy('users:users')
    
    def test_func(self):
        user = self.get_object()
        return self.request.user == user
    
    def handle_no_permission(self):
        messages.error(
            self.request,
            "У вас нет прав для изменения другого пользователя."
        )
        return redirect('users:users')
    
    def form_valid(self, form):
        messages.success(self.request, "Пользователь успешно изменен")
        return super().form_valid(form)


class UsersDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = User
    template_name = 'users/delete.html'
    context_object_name = 'user'
    success_url = reverse_lazy('users:users')

    def test_func(self):
        user = self.get_object()
        return self.request.user == user

    def handle_no_permission(self):
        messages.error(
            self.request,
            "У вас нет прав для изменения другого пользователя."
        )
        return redirect('users:users')

    def delete(self, request, *args, **kwargs):
        messages.success(request, "Пользователь успешно удален")
        return super().delete(request, *args, **kwargs)
