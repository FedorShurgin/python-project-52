from django.urls import path

from task_manager.tasks.views import TaskDeleteView, TasksCreateView, TasksView, TaskUpdateView, TaskView

app_name = 'tasks'


urlpatterns = [
    path('', TasksView.as_view(), name='tasks'),
    path('create/', TasksCreateView.as_view(), name='create'),
    path('<int:pk>/update/', TaskUpdateView.as_view(), name='update'),
    path('<int:pk>/delete/', TaskDeleteView.as_view(), name='delete'),
    path('<int:pk>/', TaskView.as_view(), name='task'),
 ]
