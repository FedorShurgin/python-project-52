from django.urls import path
from task_manager.labels.views import LabelsView, LabelsCreate

urlpatterns = [
    path('', LabelsView.as_view(), name='list_labels'),
    path('create/', LabelsCreate.as_view(), name='create_labels'),

 ]
