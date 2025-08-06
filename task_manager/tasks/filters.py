from django import forms
from django_filters import BooleanFilter, FilterSet

from task_manager.tasks.models import TasksModel


class TasksFilter(FilterSet):
    my_tasks = BooleanFilter(
        method='filter_my_tasks',
        label='Только свои задачи',
        widget=forms.CheckboxInput
    )
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.filters['labels'].label = 'Метка'
    
    def filter_my_tasks(self, queryset, name, value):
        if value:
            return queryset.filter(author=self.request.user)
        return queryset
    
    class Meta:
        model = TasksModel
        fields = ['status', 'executor', 'labels', 'my_tasks']
