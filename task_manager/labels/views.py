from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, ListView, UpdateView

from task_manager.labels.forms import LabelForm
from task_manager.labels.models import Label
from task_manager.mixins import SuccessMessageMixin, UniversalTemplateMixin


class LabelBaseView(
    UniversalTemplateMixin,
    LoginRequiredMixin,
    SuccessMessageMixin
):
    model = Label
    success_url = reverse_lazy('labels:labels')


class LabelListView(LabelBaseView, ListView):
    template_name = 'labels.html'
    context_object_name = 'labels'


class LabelCreateView(LabelBaseView, CreateView):
    form_class = LabelForm
    success_message = 'Метка успешно создана'
    page_title = "Создать метку"
    submit_text = "Создать"


class LabelUpdateView(LabelBaseView, UpdateView):
    form_class = LabelForm
    success_message = 'Метка успешно изменена'
    page_title = "Изменение метки"
    submit_text = "Изменить"


class LabelDeleteView(LabelBaseView, DeleteView):
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
