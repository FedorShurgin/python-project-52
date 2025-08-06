from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, ListView, UpdateView

from task_manager.base import SuccessMessageMixin
from task_manager.statuses.forms import StatusesCreateForm
from task_manager.statuses.models import StatusesModel


class BaseStatusView(LoginRequiredMixin, SuccessMessageMixin):
    model = StatusesModel
    success_url = reverse_lazy('statuses:statuses')


class StatusesView(BaseStatusView, ListView):
    template_name = 'statuses/statuses.html'
    context_object_name = 'statuses'


class StatusesCreateView(BaseStatusView, CreateView):
    template_name = 'statuses/create.html'
    form_class = StatusesCreateForm
    success_message = "Статус успешно создан"


class StatusesUpdateView(BaseStatusView, UpdateView):
    form_class = StatusesCreateForm
    template_name = 'statuses/update.html'
    context_object_name = 'status'
    success_message = "Статус успешно изменен"


class StatusesDeleteView(BaseStatusView, DeleteView):
    template_name = 'statuses/delete.html'
    context_object_name = 'status'
    success_message = "Статус успешно удален"
    
    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.object.tasksmodel_set.exists():
            messages.error(
                request,
                'Невозможно удалить статус, потому что он используется'
            )
            return redirect('statuses:statuses')
        return super().post(request, *args, **kwargs)
