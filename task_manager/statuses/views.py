from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, ListView, UpdateView
from django.contrib import messages


from task_manager.statuses.forms import StatusesCreateForm
from task_manager.statuses.models import StatusesModel
from task_manager.base import BaseStatusView


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
    success_message = "Статус успешно удалён"


# class StatusesCreateView(LoginRequiredMixin, CreateView):
#     model = StatusesModel
#     form_class = StatusesCreateForm
#     template_name = 'statuses/create.html'
#     success_url = reverse_lazy('statuses:statuses')

#     def form_valid(self, form):
#         messages.success(self.request, "Статус успешно создан")
#         return super().form_valid(form)


# class StatusesUpdateView(LoginRequiredMixin, UpdateView):
#     model = StatusesModel
#     form_class = StatusesCreateForm
#     template_name = 'statuses/update.html'
#     context_object_name = 'status'
#     success_url = reverse_lazy('statuses:statuses')

#     def form_valid(self, form):
#         messages.success(self.request, "Статус успешно изменен")
#         return super().form_valid(form)


# class StatusesDeleteView(LoginRequiredMixin, DeleteView):
#     model = StatusesModel
#     template_name = 'statuses/delete.html'
#     context_object_name = 'status'
#     success_url = reverse_lazy('statuses:statuses')
  