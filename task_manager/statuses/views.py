from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, ListView, UpdateView

from task_manager.statuses.forms import StatusesCreateForm
from task_manager.statuses.models import StatusesModel


class StatusesView(ListView):
    model = StatusesModel
    template_name = 'statuses/statuses.html'
    context_object_name = 'statuses'


class StatusesCreateView(LoginRequiredMixin, CreateView):
    model = StatusesModel
    form_class = StatusesCreateForm
    template_name = 'statuses/create.html'
    success_url = reverse_lazy('statuses:statuses')


class StatusesUpdateView(LoginRequiredMixin, UpdateView):
    model = StatusesModel
    form_class = StatusesCreateForm
    template_name = 'statuses/update.html'
    context_object_name = 'status'
    success_url = reverse_lazy('statuses:statuses')


class StatusesDeleteView(LoginRequiredMixin, DeleteView):
    model = StatusesModel
    template_name = 'statuses/delete.html'
    context_object_name = 'status'
    success_url = reverse_lazy('statuses:statuses')
