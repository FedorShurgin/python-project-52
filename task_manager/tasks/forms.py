from django import forms

from task_manager.tasks.models import Task


class TaskForm(forms.ModelForm):

    class Meta:
        model = Task
        fields = ['name', 'description', 'status', 'executor', 'labels']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)     
        self.fields['labels'].required = False
