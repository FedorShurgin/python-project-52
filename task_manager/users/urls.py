from django.urls import path

from .views import SignUpView, UsersDeleteView, UsersUpdateView, UsersView

app_name = 'users'


urlpatterns = [
    path('', UsersView.as_view(), name='users'),
    path('create/', SignUpView.as_view(), name='create'),
    path('<int:pk>/delete/', UsersDeleteView.as_view(), name='delete'),
    path('<int:pk>/update/', UsersUpdateView.as_view(), name='update'),
 ]
