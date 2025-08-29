from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, ListView, UpdateView

from task_manager.mixins import SuccessMessageMixin, UniversalTemplateMixin
from task_manager.statuses.forms import StatusesCreateForm
from task_manager.statuses.models import StatusesModel


class BaseStatusView(
    UniversalTemplateMixin,
    LoginRequiredMixin,
    SuccessMessageMixin
):
    model = StatusesModel
    success_url = reverse_lazy('statuses:statuses')


class StatusesView(BaseStatusView, ListView):
    template_name = 'statuses.html'
    context_object_name = 'statuses'


class StatusesCreateView(BaseStatusView, CreateView):
    form_class = StatusesCreateForm
    success_message = "Статус успешно создан"
    page_title = "Создать статус"
    submit_text = "Создать"


class StatusesUpdateView(BaseStatusView, UpdateView):
    form_class = StatusesCreateForm
    success_message = "Статус успешно изменен"
    page_title = "Изменение статуса"
    submit_text = "Изменить"


class StatusesDeleteView(BaseStatusView, DeleteView):
    success_message = "Статус успешно удален"
    page_title = "Удаление статуса"
    submit_text = "Да, удалить"
    button_class = 'btn-danger'
    confirmation_message = "Вы уверены, что хотите удалить {}"

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.object.tasksmodel_set.exists():
            messages.error(
                request,
                'Невозможно удалить статус, потому что он используется'
            )
            return redirect('statuses:statuses')
        return super().post(request, *args, **kwargs)
