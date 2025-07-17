from django import forms
from task_manager.tasks.models import TasksModel


class TasksCreateForm(forms.ModelForm):

    class Meta:
        model = TasksModel
        fields = ['name', 'description', 'status', 'executor', 'labels']
