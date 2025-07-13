from django.views.generic import ListView, CreateView
from task_manager.labels.models import LabelsModel
from task_manager.labels.forms import LabelsCreateForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy

# Create your views here.
class LabelsView(ListView):
    model = LabelsModel
    template_name = 'labels/labels.html'
    context_object_name = 'labels'

class LabelsCreate(LoginRequiredMixin, CreateView):
    model = LabelsModel
    form_class = LabelsCreateForm
    template_name = 'labels/create.html'
    success_url = reverse_lazy('list_labels')