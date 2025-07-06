from django.views.generic import ListView
from task_manager.statuses.models import StatusesModel

# Create your views here.
class StatusesView(ListView):
    model = StatusesModel
    template_name = 'statuses/statuses.html'
    context_object_name = 'statuses'