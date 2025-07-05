from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView
from task_manager.users.forms import CustomUserCreationForm
from django.contrib.auth.models import User
from django.views.generic import ListView


class SignUpView(CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'users/create.html'


class UsersView(ListView):
    model=User
    template_name = 'users/users.html'
    context_object_name = 'users'



# class ShowUser(UpdateView):
#     model = User
#     template_name = 'users/user.html'
#     fields = ('first_name', 'last_name', 'username', 'password')

