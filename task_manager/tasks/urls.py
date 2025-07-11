from django.urls import path
from task_manager.tasks.views import TasksView, TasksCreate, TaskView, TaskUpdate, TaskDelete


urlpatterns = [
    path('', TasksView.as_view(), name='list_tasks'),
    path('create/', TasksCreate.as_view(), name='create_task'),
    path('<int:pk>/update/', TaskUpdate.as_view(), name='update_task'),
    path('<int:pk>/delete/', TaskDelete.as_view(), name='delete_task'),
    path('<int:pk>/', TaskView.as_view(), name='viewing_task'),
 ]
