from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, ListView, UpdateView

from task_manager.labels.forms import LabelsCreateForm
from task_manager.labels.models import LabelsModel
from task_manager.mixins import SuccessMessageMixin, UniversalTemplateMixin


class BaseLabelsView(
    UniversalTemplateMixin,
    LoginRequiredMixin,
    SuccessMessageMixin
):
    model = LabelsModel
    success_url = reverse_lazy('labels:labels')


class LabelsView(BaseLabelsView, ListView):
    template_name = 'labels.html'
    context_object_name = 'labels'


class LabelsCreateView(BaseLabelsView, CreateView):
    form_class = LabelsCreateForm
    success_message = 'Метка успешно создана'
    page_title = "Создать метку"
    submit_text = "Создать"


class LabelsUpdateView(BaseLabelsView, UpdateView):
    form_class = LabelsCreateForm
    success_message = 'Метка успешно изменена'
    page_title = "Изменение метки"
    submit_text = "Изменить"


class LabelsDeleteView(BaseLabelsView, DeleteView):
    success_message = 'Метка успешно удалена'
    page_title = "Удаление метки"
    submit_text = "Да, удалить"
    button_class = 'btn-danger'
    confirmation_message = "Вы уверены, что хотите удалить {}"
   
    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.object.tasks.exists():
            messages.error(
                request,
                'Невозможно удалить метку, потому что она используется'
            )
            return redirect('labels:labels')
        return super().post(request, *args, **kwargs)
