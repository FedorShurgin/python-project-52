from django.urls import reverse_lazy
from django.views.generic import CreateView
from task_manager.users.forms import CustomUserCreationForm
from django.contrib.auth.models import User
from django.views.generic import ListView
from task_manager.utils import DataMixin


class SignUpView(CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'users/create.html'


class UsersView(DataMixin, ListView):
    model=User
    template_name = 'users/users.html'
    context_object_name = 'users'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        add_context = self.get_user_context(title="Пользователи")
        return {**context, **add_context}
