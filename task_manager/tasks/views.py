from django.views.generic import ListView
from task_manager.tasks.models import TasksModel
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView, DeleteView, UpdateView
from task_manager.tasks.forms import StatusesCreateForm
from django.urls import reverse_lazy


# Create your views here.
class TasksView(ListView):
    model = TasksModel
    template_name = 'tasks/tasks.html'
    context_object_name = 'tasks'

class TasksCreate(LoginRequiredMixin, CreateView):
    model = TasksModel
    form_class = StatusesCreateForm
    template_name = 'tasks/create.html'
    success_url = reverse_lazy('list_tasks')
