from django.urls import path
from task_manager.statuses.views import StatusesView, StatusCreate, UpdateStatus, DeleteStatus

urlpatterns = [
    path('', StatusesView.as_view(), name='list_statuses'),
    path('create/', StatusCreate.as_view(), name='create_status'),
    path('<int:pk>/update/', UpdateStatus.as_view(), name='update_status'),
    path('<int:pk>/delete/', DeleteStatus.as_view(), name='delete_status'),
 ]