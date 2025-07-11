from django.views.generic import ListView
from task_manager.tasks.models import TasksModel
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView, DeleteView, UpdateView, DetailView
from task_manager.tasks.forms import TasksCreateForm
from django.urls import reverse_lazy


# Create your views here.
class TasksView(ListView):
    model = TasksModel
    template_name = 'tasks/tasks.html'
    context_object_name = 'tasks'

class TasksCreate(LoginRequiredMixin, CreateView):
    model = TasksModel
    form_class = TasksCreateForm
    template_name = 'tasks/create.html'
    success_url = reverse_lazy('list_tasks')
    
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

class TaskView(LoginRequiredMixin, DetailView):
    model = TasksModel
    template_name = 'tasks/task_view.html'
    context_object_name  = 'task'

class TaskUpdate(LoginRequiredMixin, UpdateView):
    model = TasksModel
    form_class = TasksCreateForm
    template_name = 'tasks/task_update.html'
    success_url = reverse_lazy('list_tasks')

class TaskDelete(LoginRequiredMixin, DeleteView):
    model = TasksModel
    template_name = 'tasks/task_delete.html'
    success_url = reverse_lazy('list_tasks')
    
    def test_func(self):
        obj = self.get_object()
        return obj.author == self.request.user
