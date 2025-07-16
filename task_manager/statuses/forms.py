from django import forms
from task_manager.statuses.models import StatusesModel

class StatusesCreateForm(forms.ModelForm):
    
    class Meta:
        model = StatusesModel
        fields = ['name']
