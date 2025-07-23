from django_filters import FilterSet, BooleanFilter
from task_manager.tasks.models import TasksModel
from django import forms


class TasksFilter(FilterSet):
    my_tasks = BooleanFilter(
        method='filter_my_tasks',
        label='Только свои задачи',
        widget=forms.CheckboxInput
    )
    
    def filter_my_tasks(self, queryset, name, value):
        if value:
            return queryset.filter(author=self.request.user)
        return queryset
    
    class Meta:
        model = TasksModel
        fields = ['status', 'executor', 'labels', 'my_tasks']
