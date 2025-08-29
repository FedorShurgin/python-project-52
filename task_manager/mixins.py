from django.contrib import messages


class SuccessMessageMixin:
    
    def form_valid(self, form):
        messages.success(self.request, self.success_message)
        return super().form_valid(form)


class UniversalTemplateMixin:
    template_name = 'form.html'
    page_title = None
    submit_text = None
    button_class = 'btn-primary'
    confirmation_message = None
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.page_title:
            context['page_title'] = self.page_title
        if self.submit_text:
            context['submit_text'] = self.submit_text
        if self.button_class:
            context['button_class'] = self.button_class
        if self.confirmation_message:
            context['confirmation_message'] = self.confirmation_message.format(
                self.object.name
            )
        return context
