from django.shortcuts import render, redirect
from django.views import View
from task_manager.users.models import UsersModels
from task_manager.users.forms import UserForms


class UserCreateView(View):
    
    def get(self, request, *args, **kwargs):
        form = UserForms()
        return render(request, 'users/create.html', {'form': form})
    
    def post(self, request, *args, **kwargs):
        form = UserForms(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
        
        return render(request, 'users/create.html', {'form': form})