from django.urls import path

from task_manager.labels.views import (
    LabelsCreateView,
    LabelsDeleteView,
    LabelsUpdateView,
    LabelsView,
)

app_name = 'labels'


urlpatterns = [
    path('', LabelsView.as_view(), name='labels'),
    path('create/', LabelsCreateView.as_view(), name='create'),
    path('<int:pk>/update/', LabelsUpdateView.as_view(), name='update'),
    path('<int:pk>/delete/', LabelsDeleteView.as_view(), name='delete'),
 ]
