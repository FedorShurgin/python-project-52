from django.urls import reverse_lazy
from django.views.generic import CreateView
from task_manager.users.forms import CustomUserCreationForm
from django.views import View
from django.contrib.auth.models import User
from django.shortcuts import render


class SignUpView(CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'users/create.html'
    
class UsersView(View):
    
    def get(self, request, *args, **kwargs):
        users = User.objects.all
        return render(
            request,
            'users/users.html',
            context={'users': users}
            )
