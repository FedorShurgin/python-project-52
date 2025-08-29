from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import DeleteView, ListView, UpdateView

from task_manager.mixins import SuccessMessageMixin, UniversalTemplateMixin
from task_manager.users.forms import CustomUserCreationForm


class BaseView(
    UniversalTemplateMixin,
    LoginRequiredMixin,
    UserPassesTestMixin,
    SuccessMessageMixin
):
    model = User
    success_url = reverse_lazy('users:users')
    error_message = "У вас нет прав для изменения другого пользователя."
    
    def test_func(self):
        user = self.get_object()
        return self.request.user == user
    
    def handle_no_permission(self):
        messages.error(self.request, self.error_message)
        return redirect(self.success_url)


class UsersView(ListView):
    model = User
    template_name = 'users.html'
    context_object_name = 'users'

   
class UsersUpdateView(BaseView, UpdateView):
    form_class = CustomUserCreationForm
    success_message = "Пользователь успешно изменен"
    page_title = "Изменение пользователя"
    submit_text = "Изменить"


class UsersDeleteView(BaseView, DeleteView):
    success_message = "Пользователь успешно удален"
    page_title = "Удаление"
    submit_text = "Да, удалить"
    button_class = 'btn-danger'
