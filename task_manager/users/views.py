from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, UpdateView
from task_manager.users.forms import CustomUserCreationForm, CustomUserUpdateForm
from django.contrib.auth.models import User
from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin


class SignUpView(CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'users/create.html'


class UsersView(ListView):
    model=User
    template_name = 'users/users.html'
    context_object_name = 'users'


class UpdateUser(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = User
    form_class = CustomUserUpdateForm
    template_name = 'users/user.html'
    context_object_name = 'user'
    success_url = reverse_lazy('list_users')
    #userpassestestmixin пользователь может изменять токо себя
    
    def test_func(self):
        user = self.get_object()
        return self.request.user == user

class UserDeleteView(DeleteView):
    model = User
    template_name = 'users/delete.html'
    success_url = reverse_lazy('home')