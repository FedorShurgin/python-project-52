from django.views.generic import ListView
from task_manager.statuses.models import StatusesModel
from django.views.generic import CreateView, DeleteView, UpdateView
from task_manager.statuses.forms import StatusesCreateForm
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin


class StatusesView(ListView):
    model = StatusesModel
    template_name = 'statuses/statuses.html'
    context_object_name = 'statuses'


class StatusesCreateView(LoginRequiredMixin, CreateView):
    model = StatusesModel
    form_class = StatusesCreateForm
    template_name = 'statuses/create.html'
    success_url = reverse_lazy('statuses')


class StatusesUpdateView(LoginRequiredMixin, UpdateView):
    model = StatusesModel
    form_class = StatusesCreateForm
    template_name = 'statuses/status.html'
    context_object_name = 'status'
    success_url = reverse_lazy('statuses')


class StatusesDeleteView(LoginRequiredMixin, DeleteView):
    moStatusDeleteViewdel = StatusesModel
    template_name = 'statuses/delete.html'
    context_object_name = 'status'
    success_url = reverse_lazy('statuses')
