from django.urls import path
from task_manager.tasks.views import TasksView, TasksCreate


urlpatterns = [
    path('', TasksView.as_view(), name='list_tasks'),
    path('create/', TasksCreate.as_view(), name='create_task'),
 ]
