from task_manager.tasks.models import TasksModel
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import CreateView, DeleteView, UpdateView, DetailView
from task_manager.tasks.forms import TasksCreateForm
from django.urls import reverse_lazy
from django.contrib import messages
from django.shortcuts import redirect
from django_filters.views import FilterView
from task_manager.tasks.filters import TasksFilter


class TasksView(FilterView):
    model = TasksModel
    filterset_class = TasksFilter
    template_name = 'tasks/tasks.html'
    context_object_name = 'tasks'
    

class TasksCreateView(LoginRequiredMixin, CreateView):
    model = TasksModel
    form_class = TasksCreateForm
    template_name = 'tasks/create.html'
    success_url = reverse_lazy('tasks:tasks')
    
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class TaskView(LoginRequiredMixin, DetailView):
    model = TasksModel
    template_name = 'tasks/task.html'
    context_object_name  = 'task'


class TaskUpdateView(LoginRequiredMixin, UpdateView):
    model = TasksModel
    form_class = TasksCreateForm
    template_name = 'tasks/update.html'
    success_url = reverse_lazy('tasks:tasks')


class TaskDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = TasksModel
    template_name = 'tasks/delete.html'
    success_url = reverse_lazy('tasks:tasks')
    
    def test_func(self):
        obj = self.get_object()
        return obj.author == self.request.user
    
    def handle_no_permission(self):
        messages.error(self.request, "Задачу может удалить только ее автор")
        return redirect('tasks:tasks')
