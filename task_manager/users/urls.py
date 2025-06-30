from django.urls import path
from .views import SignUpView, UsersView


urlpatterns = [
    path('',UsersView.as_view(), name='list_users'),
    path('create/', SignUpView.as_view(), name='create_user'),
]
