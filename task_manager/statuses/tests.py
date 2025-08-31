from django.contrib.auth import get_user_model
from django.contrib.messages import get_messages
from django.test import TestCase
from django.urls import reverse

from task_manager.statuses.forms import StatusForm
from task_manager.statuses.models import StatusesModel
from task_manager.tasks.models import TasksModel

User = get_user_model()


class StatusListViewTest(TestCase):
    
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create(
            username='test_username',
        )

        cls.user.set_password('test_password123')
        cls.user.save()
        
        number_of_statuses = 12
        for status_num in range(number_of_statuses):
            StatusesModel.objects.create(
                name=f'Status {status_num}',
                author=cls.user,
            )

    def setUp(self):
        self.client.login(
            username='test_username',
            password='test_password123',
        )

    def test_statuses_view_uses_correct_template(self):
        resp = self.client.get(reverse('statuses:statuses'))
        self.assertTemplateUsed(resp, 'statuses.html')
        self.assertEqual(resp.status_code, 200)


class StatusCreateViewTest(TestCase):
    
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create(
            username='test_username',
        )

        cls.user.set_password('test_password123')
        cls.user.save()
        
        cls.valid_data = {'name': 'New_Status'}

    def setUp(self):
        self.client.login(
            username='test_username',
            password='test_password123',
        )

    def test_create_view_uses_correct_template_form(self):
        resp = self.client.get(reverse('statuses:create'))
        self.assertTemplateUsed(resp, 'form.html')
        self.assertIsInstance(resp.context['form'], StatusForm)
        self.assertEqual(resp.status_code, 200)

    def test_create_view_displays_correct_content(self):
        resp = self.client.get(reverse('statuses:create'))
        
        self.assertContains(resp, 'method="post"')

        self.assertContains(resp, 'Создать статус', status_code=200)
        self.assertContains(resp, 'Имя')
        
        self.assertContains(resp, 'type="submit"')
        self.assertContains(resp, 'Создать')        
    
    def test_create_status_success(self):
        resp = self.client.post(
            reverse('statuses:create'),
            data=self.valid_data
        )
        self.assertRedirects(resp, reverse('statuses:statuses'))
        
        messages = list(get_messages(resp.wsgi_request))
        self.assertEqual(str(messages[0]), "Статус успешно создан")
        
    def test_created_status_exists_in_db(self):
        test_status_name = "Test status"
        
        self.client.post(
            reverse('statuses:create'),
            data={'name': test_status_name}
        )
        self.assertTrue(
            StatusesModel.objects.filter(name=test_status_name).exists(),
            "Статус с указанным именем должен существовать в БД"
        )
  
              
class StatusUpdateViewTest(TestCase):
    
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create(
            username='test_username',
        )

        cls.user.set_password('test_password123')
        cls.user.save()

        cls.status = StatusesModel.objects.create(
            name='Original_Status',
            author=cls.user
        )
        cls.valid_data = {'name': 'Updated_Status'}
    
    def setUp(self):
        self.client.login(
            username='test_username',
            password='test_password123',
        )
            
    def test_update_view_uses_correct_template_form(self):
        resp = self.client.get(
            reverse('statuses:update', kwargs={'pk': self.status.pk})
        )
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'form.html')
        self.assertIsInstance(resp.context['form'], StatusForm)
        
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

    def test_create_view_displays_correct_content(self):
        resp = self.client.get(reverse(
            'statuses:update',
            kwargs={'pk': self.status.pk}
            )
        )
        
        self.assertContains(resp, 'method="post"')

        self.assertContains(resp, 'Изменение статуса')
        self.assertContains(resp, 'Original_Status')
        self.assertContains(resp, 'Имя')
        
        self.assertContains(resp, 'type="submit"')
        self.assertContains(resp, 'Изменить') 


class StatusDeleteViewTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create(
            username='test_username',
        )

        cls.user.set_password('test_password123')
        cls.user.save()
        
        cls.status = StatusesModel.objects.create(
            name='Status_delete',
            author=cls.user
        )
    
    def setUp(self):
        self.client.login(
            username='test_username',
            password='test_password123',
        )

    def test_delete_view_uses_correct_template(self):
        resp = self.client.get(
            reverse('statuses:delete', kwargs={'pk': self.status.pk})
        )
        self.assertTemplateUsed(resp, 'form.html')
        self.assertEqual(resp.status_code, 200)
        
    def test_delete_status_success(self):
        resp = self.client.post(
            reverse('statuses:delete', kwargs={'pk': self.status.pk})
        )
        self.assertRedirects(resp, reverse('statuses:statuses'))
        
        messages = list(get_messages(resp.wsgi_request))
        self.assertEqual(str(messages[0]), "Статус успешно удален")
        
    def test_cannot_delete_used_status(self):
        TasksModel.objects.create(
            name="New_Task",
            status=self.status,
        )
        initial_count = StatusesModel.objects.count()
        resp = self.client.post(
            reverse('statuses:delete', kwargs={'pk': self.status.pk})
        )
        self.assertEqual(StatusesModel.objects.count(), initial_count)
        
        messages = list(get_messages(resp.wsgi_request))
        self.assertEqual(
            str(messages[0]),
            'Невозможно удалить статус, потому что он используется'
        )

    def test_delete_view_displays_correct_content(self):
        status = self.status.pk
                
        resp = self.client.get(
            reverse(
                'statuses:delete',
                kwargs={'pk': status}
                )
            )
        
        expected_message = f'Вы уверены, что хотите удалить {self.status.name}'
        
        self.assertContains(resp, 'method="post"', status_code=200)
        self.assertContains(resp, 'Удаление статуса')
        self.assertContains(resp, expected_message)
        self.assertContains(resp, 'type="submit"')
        self.assertContains(resp, 'Да, удалить')
