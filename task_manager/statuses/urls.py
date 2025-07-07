from django.urls import path
from task_manager.statuses.views import StatusesView, StatusCreate

urlpatterns = [
    path('', StatusesView.as_view(), name='list_statuses'),
    path('create/', StatusCreate.as_view(), name='create_status'),
 ]