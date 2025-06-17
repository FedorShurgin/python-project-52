from django.urls import path
from .views import SignUpView

urlpatterns = [
    path('create/', SignUpView.as_view(), name='create_user')
]
