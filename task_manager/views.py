from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.views import LoginView
from django.shortcuts import redirect


class MyLoginView(LoginView):
    template_name = 'login.html'
    
    def form_valid(self, form):
        super().form_valid(form)
        messages.success(self.request, "Вы залогинены")
        return redirect('home') 


def logout_user(request):
    logout(request)
    messages.success(request, "Вы разлогинены")
    return redirect('home')
