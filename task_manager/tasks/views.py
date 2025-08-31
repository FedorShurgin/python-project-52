from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, DetailView, UpdateView
from django_filters.views import FilterView

from task_manager.mixins import SuccessMessageMixin, UniversalTemplateMixin
from task_manager.tasks.filters import TaskFilter
from task_manager.tasks.forms import TaskForm
from task_manager.tasks.models import TasksModel


class TaskBaseView(
    UniversalTemplateMixin,
    LoginRequiredMixin,
    SuccessMessageMixin
):
    model = TasksModel
    success_url = reverse_lazy('tasks:tasks')


class TaskListView(TaskBaseView, FilterView):
    filterset_class = TaskFilter
    template_name = 'tasks.html'
    context_object_name = 'tasks'
    

class TaskCreateView(TaskBaseView, CreateView):
    form_class = TaskForm
    success_message = 'Задача успешно создана'
    page_title = "Создать задачу"
    submit_text = "Создать"
    
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class TaskDetailView(TaskBaseView, DetailView):
    template_name = 'task.html'
    context_object_name = 'task'


class TaskUpdateView(TaskBaseView, UpdateView):
    form_class = TaskForm
    success_message = 'Задача успешно изменена'
    page_title = "Изменение задачи"
    submit_text = "Изменить"


class TaskDeleteView(TaskBaseView, UserPassesTestMixin, DeleteView):
    success_message = 'Задача успешно удалена'
    page_title = "Удаление"
    submit_text = "Да, удалить"
    button_class = 'btn-danger'
    
    def test_func(self):
        obj = self.get_object()
        return obj.author == self.request.user
    
    def handle_no_permission(self):
        messages.error(
            self.request,
            "Задачу может удалить только ее автор"
        )
        return redirect('tasks:tasks')
