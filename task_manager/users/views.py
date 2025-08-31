from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import DeleteView, ListView, UpdateView

from task_manager.mixins import SuccessMessageMixin, UniversalTemplateMixin
from task_manager.users.forms import UserCreationForm

User = get_user_model()


class UserBaseView(
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


class UserListView(ListView):
    model = User
    template_name = 'users.html'
    context_object_name = 'users'

   
class UserUpdateView(UserBaseView, UpdateView):
    form_class = UserCreationForm
    success_message = "Пользователь успешно изменен"
    page_title = "Изменение пользователя"
    submit_text = "Изменить"


class UserDeleteView(UserBaseView, DeleteView):
    success_message = "Пользователь успешно удален"
    page_title = "Удаление"
    submit_text = "Да, удалить"
    button_class = 'btn-danger'
