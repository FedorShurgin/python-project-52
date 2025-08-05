from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.contrib import messages

from task_manager.statuses.models import StatusesModel


class SuccessMessageMixin:
    
    def form_valid(self, form):
        messages.success(self.request, self.success_message)
        return super().form_valid(form)


class BaseStatusView(LoginRequiredMixin, SuccessMessageMixin):
    model = StatusesModel
    success_url = reverse_lazy('statuses:statuses')
