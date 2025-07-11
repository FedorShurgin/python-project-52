from django.contrib.auth import logout
from django.shortcuts import redirect
from django.http import HttpResponse



def logout_user(request):
    logout(request)
    return redirect('home')

def labels(request):
    return HttpResponse('Страница с метками!')
