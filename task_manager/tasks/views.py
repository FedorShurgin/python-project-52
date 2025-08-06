from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, DetailView, UpdateView
from django_filters.views import FilterView

from task_manager.tasks.filters import TasksFilter
from task_manager.tasks.forms import TasksCreateForm
from task_manager.tasks.models import TasksModel
from task_manager.base import SuccessMessageMixin


class BaseTasksView(LoginRequiredMixin, SuccessMessageMixin):
    model = TasksModel
    success_url = reverse_lazy('tasks:tasks')



class TasksView(BaseTasksView, FilterView):
    filterset_class = TasksFilter
    template_name = 'tasks/tasks.html'
    context_object_name = 'tasks'
    

class TasksCreateView(BaseTasksView, CreateView):
    form_class = TasksCreateForm
    template_name = 'tasks/create.html'
    success_message = 'Задача успешно создана'
    
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class TaskView(BaseTasksView, DetailView):
    template_name = 'tasks/task.html'
    context_object_name = 'task'


class TaskUpdateView(BaseTasksView, UpdateView):
    form_class = TasksCreateForm
    template_name = 'tasks/update.html'
    success_message = 'Задача успешно изменена'



class TaskDeleteView(BaseTasksView, UserPassesTestMixin, DeleteView):
    template_name = 'tasks/delete.html'
    success_message = 'Задача успешно удалена'
    
    def test_func(self):
        obj = self.get_object()
        return obj.author == self.request.user
    
    def handle_no_permission(self):
        messages.error(self.request, "Задачу может удалить только ее автор")
        return redirect('tasks:tasks')
