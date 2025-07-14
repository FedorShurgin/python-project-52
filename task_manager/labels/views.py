from django.views.generic import ListView, CreateView, UpdateView, DeleteView
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

class LabelUpdate(LoginRequiredMixin, UpdateView):
    model = LabelsModel
    form_class = LabelsCreateForm
    template_name = 'labels/update.html'
    success_url = reverse_lazy('list_labels')

class LabelDelete(LoginRequiredMixin, DeleteView):
    model = LabelsModel
    template_name = 'labels/delete.html'
    context_object_name = 'label'
    success_url = reverse_lazy('list_labels')
