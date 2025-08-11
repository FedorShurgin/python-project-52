from django.test import TestCase
from django.contrib.messages import get_messages
from django.urls import reverse

from task_manager.statuses.models import StatusesModel
from task_manager.tasks.models import TasksModel
from task_manager.statuses.forms import StatusesCreateForm
from django.contrib.auth.models import User


class StatusesViewTest(TestCase):
    
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create(
            first_name = 'test_mame',
            last_name = 'test_Surname',
            username = 'test_username',
            password = 'test_password123',
        )

        number_of_statuses = 12
        for status_num in range(number_of_statuses):
            StatusesModel.objects.create(
                name=f'Status {status_num}',
                author=cls.user
            )

    def setUp(self):
        self.client.login(
            username='test_username',
            password='test_password123',
        )

    def test_statuses_view_url_exists(self):
        resp = self.client.get(reverse('statuses:statuses'))
        self.assertEqual(resp.status_code, 200)

    def test_statuses_view_uses_correct_template(self):
        resp = self.client.get(reverse('statuses:statuses'))
        self.assertTemplateUsed(resp, 'statuses/statuses.html')

class StatusesCreateViewTest(TestCase):
    
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(
            first_name = 'test_mame',
            last_name = 'test_surname',
            username = 'test_username',
            password = 'test_password123',
        )
        
        cls.valid_data = {'name': 'New_Status'}

    def setUp(self):
        self.client.login(
            username='test_username',
            password='test_password123',
        )
        
    def test_create_view_url_exists(self):
        resp = self.client.get(reverse('statuses:create'))
        self.assertEqual(resp.status_code, 200)
    
    def test_create_view_uses_correct_template(self):
        resp = self.client.get(reverse('statuses:create'))
        self.assertTemplateUsed(resp, 'statuses/create.html')
    
    def test_create_view_uses_correct_form(self):
        resp = self.client.get(reverse('statuses:create'))
        self.assertIsInstance(resp.context['form'], StatusesCreateForm)
    
    def test_create_status_success(self):
        resp = self.client.post(
            reverse('statuses:create'),
            data=self.valid_data
        )
        self.assertRedirects(resp, reverse('statuses:statuses'))
        
        messages = list(get_messages(resp.wsgi_request))
        self.assertEqual(str(messages[0]), "Статус успешно создан")
        
class StatusesUpdateViewTest(TestCase):
    
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(
            first_name = 'test_mame',
            last_name = 'test_surname',
            username = 'test_username',
            password = 'test_password123',
        )
        
        cls.status = StatusesModel.objects.create(
            name = 'status',
        )
        
        cls.status = StatusesModel.objects.create(
            name='Original Status',
            author=cls.user
        )
        cls.valid_data = {'name': 'Updated_Status'}
    
    def setUp(self):
        self.client.login(
            username='test_username',
            password='test_password123',
        )
        
    def test_update_view_url_exists(self):
        resp = self.client.get(
            reverse('statuses:update', kwargs={'pk': self.status.pk})
        )
        self.assertEqual(resp.status_code, 200)
    
    def test_update_view_uses_correct_template(self):
        resp = self.client.get(
            reverse('statuses:update', kwargs={'pk': self.status.pk})
        )
        self.assertTemplateUsed(resp, 'statuses/update.html')
        
    def test_update_status_success(self):
        resp = self.client.post(
            reverse('statuses:update', kwargs={'pk': self.status.pk}),
            data=self.valid_data
        )
        self.assertRedirects(resp, reverse('statuses:statuses'))
        self.status.refresh_from_db()
        self.assertEqual(self.status.name, 'Updated_Status')
        
        messages = list(get_messages(resp.wsgi_request))
        self.assertEqual(str(messages[0]), "Статус успешно изменен")
        
class StatusesDeleteViewTest(TestCase):
    
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(
            first_name = 'test_mame',
            last_name = 'test_surname',
            username = 'test_username',
            password = 'test_password123',
        )
        
        cls.status = StatusesModel.objects.create(
            name='Status_delete',
            author=cls.user
        )
    
    def setUp(self):
        self.client.login(
            username='test_username',
            password='test_password123',
        )
    
    def test_delete_view_url_exists(self):
        resp = self.client.get(
            reverse('statuses:delete', kwargs={'pk': self.status.pk})
        )
        self.assertEqual(resp.status_code, 200)
        
    def test_delete_view_uses_correct_template(self):
        resp = self.client.get(
            reverse('statuses:delete', kwargs={'pk': self.status.pk})
        )
        self.assertTemplateUsed(resp, 'statuses/delete.html')
        
    def test_delete_status_success(self):
        resp = self.client.post(
            reverse('statuses:delete', kwargs={'pk': self.status.pk})
        )
        self.assertRedirects(resp, reverse('statuses:statuses'))
        
        messages = list(get_messages(resp.wsgi_request))
        self.assertEqual(str(messages[0]), "Статус успешно удален")
        
    def test_delete_view_requires_login(self):
        task = TasksModel.objects.create(status=self.status)
        resp = self.client.post(
            reverse('statuses:delete', kwargs={'pk': self.status.pk})
        )
        
        self.assertContains(
            resp,
            'Невозможно удалить статус, потому что он используется'
        )
