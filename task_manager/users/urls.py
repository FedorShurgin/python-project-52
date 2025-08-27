from django.urls import path

from .views import UsersDeleteView, UsersUpdateView, UsersView

app_name = 'users'


urlpatterns = [
    path('', UsersView.as_view(), name='users'),
    path('<int:pk>/delete/', UsersDeleteView.as_view(), name='delete'),
    path('<int:pk>/update/', UsersUpdateView.as_view(), name='update'),
 ]
