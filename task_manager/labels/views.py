from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, ListView, UpdateView

from task_manager.labels.forms import LabelsCreateForm
from task_manager.labels.models import LabelsModel
from task_manager.mixins import SuccessMessageMixin


class BaseLabelsView(LoginRequiredMixin, SuccessMessageMixin):
    model = LabelsModel
    success_url = reverse_lazy('labels:labels')


class LabelsView(BaseLabelsView, ListView):
    template_name = 'labels/labels.html'
    context_object_name = 'labels'


class LabelsCreateView(BaseLabelsView, CreateView):
    form_class = LabelsCreateForm
    template_name = 'labels/create.html'
    success_message = 'Метка успешно создана'


class LabelsUpdateView(BaseLabelsView, UpdateView):
    form_class = LabelsCreateForm
    template_name = 'labels/update.html'
    success_message = 'Метка успешно изменена'


class LabelsDeleteView(BaseLabelsView, DeleteView):
    template_name = 'labels/delete.html'
    context_object_name = 'label'
    success_message = 'Метка успешно удалена'
   
    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.object.tasks.exists():
            messages.error(
                request,
                'Невозможно удалить метку, потому что она используется'
            )
            return redirect('labels:labels')
        return super().post(request, *args, **kwargs)
