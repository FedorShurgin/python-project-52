from django.urls import path
from task_manager.statuses.views import StatusesView

urlpatterns = [
    path('',StatusesView.as_view(), name='list_statuses'),
 ]