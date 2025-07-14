from django.urls import path
from task_manager.labels.views import LabelsView, LabelsCreate, LabelUpdate, LabelDelete

urlpatterns = [
    path('', LabelsView.as_view(), name='list_labels'),
    path('create/', LabelsCreate.as_view(), name='create_labels'),
    path('<int:pk>/update/', LabelUpdate.as_view(), name='update_label'),
    path('<int:pk>/delete/', LabelDelete.as_view(), name='delete_label'),
 ]
