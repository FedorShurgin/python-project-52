from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, ListView, UpdateView

from task_manager.labels.forms import LabelsCreateForm
from task_manager.labels.models import LabelsModel


class LabelsView(ListView):
    model = LabelsModel
    template_name = 'labels/labels.html'
    context_object_name = 'labels'


class LabelsCreateView(LoginRequiredMixin, CreateView):
    model = LabelsModel
    form_class = LabelsCreateForm
    template_name = 'labels/create.html'
    success_url = reverse_lazy('labels:labels')


class LabelsUpdateView(LoginRequiredMixin, UpdateView):
    model = LabelsModel
    form_class = LabelsCreateForm
    template_name = 'labels/update.html'
    success_url = reverse_lazy('labels:labels')


class LabelsDeleteView(LoginRequiredMixin, DeleteView):
    model = LabelsModel
    template_name = 'labels/delete.html'
    context_object_name = 'label'
    success_url = reverse_lazy('labels:labels')
   
    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.object.tasks.exists():
            messages.error(request, 'Невозможно удалить метку, потому что она используется')
            return redirect('labels:labels')
        return super().post(request, *args, **kwargs)
