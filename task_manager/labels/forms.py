from django import forms

from task_manager.labels.models import LabelsModel


class LabelsCreateForm(forms.ModelForm):
    
    class Meta:
        model = LabelsModel
        fields = ['name']
