from django.urls import path

from task_manager.statuses.views import (
    StatusesCreateView,
    StatusesDeleteView,
    StatusesUpdateView,
    StatusesView,
)

app_name = 'statuses'


urlpatterns = [
    path('', StatusesView.as_view(), name='statuses'),
    path('create/', StatusesCreateView.as_view(), name='create'),
    path('<int:pk>/update/', StatusesUpdateView.as_view(), name='update'),
    path('<int:pk>/delete/', StatusesDeleteView.as_view(), name='delete'),
 ]
