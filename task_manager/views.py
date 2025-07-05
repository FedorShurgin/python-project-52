from django.contrib.auth import logout
from django.shortcuts import redirect
from django.http import HttpResponse



def logout_user(request):
    logout(request)
    return redirect('home')

def statuses(request):
    return HttpResponse('Страница со статусами!')

def labels(request):
    return HttpResponse('Страница с метками!')

def tasks(request):
    return HttpResponse('Страница с задачами!')