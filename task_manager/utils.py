menu = [
    {'title':'Пользователи', 'url_name':'list_users'},
    {'title':'Статусы', 'url_name':'statuses'},
    {'title':'Метки', 'url_name':'labels'},
    {'title':'Задачи', 'url_name':'tasks'},
    ]


class DataMixin:
    def get_user_context(self, **kwargs):
        context = kwargs
        if not self.request.user.is_authenticated:
             menu_not_login = menu[0]
             context['menu'] = menu_not_login
             return context
        context['menu'] = menu
        return context
