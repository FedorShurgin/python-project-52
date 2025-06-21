from django.urls import path
from .views import SignUpView, UsersView
from django.views.generic.base import TemplateView


urlpatterns = [
    path('',UsersView.as_view(), name='list_users'),
    path('create/', SignUpView.as_view(), name='create_user'),
]
