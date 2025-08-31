from django.urls import path

from .views import UserDeleteView, UserListView, UserUpdateView

app_name = 'users'


urlpatterns = [
    path('', UserListView.as_view(), name='users'),
    path('<int:pk>/delete/', UserDeleteView.as_view(), name='delete'),
    path('<int:pk>/update/', UserUpdateView.as_view(), name='update'),
 ]
