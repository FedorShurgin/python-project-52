from django_filters import FilterSet
from task_manager.tasks.models import TasksModel

class TasksFilter(FilterSet):
    
    class Meta:
        model = TasksModel
        fields = ['status', 'executor', 'labels']