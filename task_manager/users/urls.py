from django.urls import path
from .views import SignUpView, UsersView, UserDeleteView, UpdateUser


urlpatterns = [
    path('',UsersView.as_view(), name='list_users'),
    path('create/', SignUpView.as_view(), name='create_user'),
    path('<int:pk>/delete/',UserDeleteView.as_view(), name='delete_user' ),
    path('<int:pk>/update/', UpdateUser.as_view(), name='update_user'),
 ]
