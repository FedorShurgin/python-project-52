from django.contrib.auth import logout
from django.shortcuts import redirect
from django.http import HttpResponse
from django.contrib.auth.views import LoginView
from django.contrib.auth.forms import AuthenticationForm
from task_manager.utils import DataMixin
from django.views.generic.base import TemplateView


class LoginUser(DataMixin, LoginView):
    form_class = AuthenticationForm
    template_name = 'login.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        add_context = self.get_user_context(title="Вход")
        return {**context, **add_context}

class MyTemplateView(DataMixin, TemplateView):
    template_name = 'index.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        add_context = self.get_user_context()
        return {**context, **add_context}
    



def logout_user(request):
    logout(request)
    return redirect('home')

def statuses(request):
    return HttpResponse('Страница со статусами!')

def labels(request):
    return HttpResponse('Страница с метками!')

def tasks(request):
    return HttpResponse('Страница с задачами!')