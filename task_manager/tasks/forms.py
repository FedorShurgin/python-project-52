from django import forms

from task_manager.tasks.models import TasksModel


class TasksCreateForm(forms.ModelForm):

    class Meta:
        model = TasksModel
        fields = ['name', 'description', 'status', 'executor', 'labels']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.fields['executor'].label_from_instance = lambda user: (
            f"{user.first_name} {user.last_name}".strip() or user.username
        )
