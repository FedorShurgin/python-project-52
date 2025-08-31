from django.contrib.auth import get_user_model
from django.contrib.messages import get_messages
from django.test import TestCase
from django.urls import reverse

from task_manager.labels.forms import LabelForm
from task_manager.labels.models import Label
from task_manager.tasks.models import Task

User = get_user_model()


class LabelListViewTest(TestCase):
    
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create(
            username='test_username',
        )

        cls.user.set_password('test_password123')
        cls.user.save()
        
        number_of_labels = 12
        for label_num in range(number_of_labels):
            Label.objects.create(
                name=f'Labels {label_num}',
                author=cls.user,
            )

    def setUp(self):
        self.client.login(
            username='test_username',
            password='test_password123',
        )

    def test_labels_view_uses_correct_template(self):
        resp = self.client.get(reverse('labels:labels'))
        self.assertTemplateUsed(resp, 'labels.html')
        self.assertEqual(resp.status_code, 200)


class LabelCreateViewTest(TestCase):
    
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create(
            username='test_username',
        )

        cls.user.set_password('test_password123')
        cls.user.save()
        
        cls.valid_data = {'name': 'New_Labels'}

    def setUp(self):
        self.client.login(
            username='test_username',
            password='test_password123',
        )

    def test_labels_view_uses_correct_template_form(self):
        resp = self.client.get(reverse('labels:create'))
        self.assertTemplateUsed(resp, 'form.html')
        self.assertIsInstance(resp.context['form'], LabelForm)
        self.assertEqual(resp.status_code, 200)

    def test_labels_view_displays_correct_content(self):
        resp = self.client.get(reverse('labels:create'))
        
        self.assertContains(resp, 'method="post"')

        self.assertContains(resp, 'Создать метку', status_code=200)
        self.assertContains(resp, 'Имя')
        
        self.assertContains(resp, 'type="submit"')
        self.assertContains(resp, 'Создать')

    def test_create_label_success(self):
        resp = self.client.post(
            reverse('labels:create'),
            data=self.valid_data
        )
        self.assertRedirects(resp, reverse('labels:labels'))
        
        messages = list(get_messages(resp.wsgi_request))
        self.assertEqual(str(messages[0]), "Метка успешно создана")

    def test_created_label_exists_in_db(self):
        test_label_name = "Test labels"
        
        self.client.post(
            reverse('labels:create'),
            data={'name': test_label_name}
        )
        self.assertTrue(
            Label.objects.filter(name=test_label_name).exists(),
            "Метка с указанным именем должена существовать в БД"
        )


class LabelUpdateViewTest(TestCase):
    
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create(
            username='test_username',
        )

        cls.user.set_password('test_password123')
        cls.user.save()    
        
        cls.label = Label.objects.create(
            name='Original_Label',
            author=cls.user
        )
        cls.valid_data = {'name': 'Updated_Label'}
    
    def setUp(self):
        self.client.login(
            username='test_username',
            password='test_password123',
        )

    def test_update_view_uses_correct_template(self):
        resp = self.client.get(
            reverse('labels:update', kwargs={'pk': self.label.pk})
        )
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'form.html')
        self.assertIsInstance(resp.context['form'], LabelForm)

    def test_update_label_success(self):
        resp = self.client.post(
            reverse('labels:update', kwargs={'pk': self.label.pk}),
            data=self.valid_data
        )
        self.assertRedirects(resp, reverse('labels:labels'))
        self.label.refresh_from_db()
        self.assertEqual(self.label.name, 'Updated_Label')
        
        messages = list(get_messages(resp.wsgi_request))
        self.assertEqual(str(messages[0]), "Метка успешно изменена")

    def test_labels_view_displays_correct_content(self):
        resp = self.client.get(reverse(
            'labels:update',
            kwargs={'pk': self.label.pk}
            )
        )
        
        self.assertContains(resp, 'method="post"')

        self.assertContains(resp, 'Изменение метки', status_code=200)
        self.assertContains(resp, 'Имя')
        self.assertContains(resp, 'Original_Label')
        
        self.assertContains(resp, 'type="submit"')
        self.assertContains(resp, 'Изменить')


class LabelDeleteViewTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create(
            username='test_username',
        )

        cls.user.set_password('test_password123')
        cls.user.save()
        
        cls.label = Label.objects.create(
            name='Label_delete',
            author=cls.user
        )
    
    def setUp(self):
        self.client.login(
            username='test_username',
            password='test_password123',
        )

    def test_delete_view_uses_correct_template(self):
        resp = self.client.get(
            reverse('labels:delete', kwargs={'pk': self.label.pk})
        )
        self.assertTemplateUsed(resp, 'form.html')
        self.assertEqual(resp.status_code, 200)

    def test_delete_label_success(self):
        resp = self.client.post(
            reverse('labels:delete', kwargs={'pk': self.label.pk})
        )
        self.assertRedirects(resp, reverse('labels:labels'))
        
        messages = list(get_messages(resp.wsgi_request))
        self.assertEqual(str(messages[0]), "Метка успешно удалена")

    def test_cannot_delete_used_label(self):
        task = Task.objects.create(
            name="New_Task",
        )
        
        task.labels.add(self.label)
        
        initial_count = Label.objects.count()
        resp = self.client.post(
            reverse('labels:delete', kwargs={'pk': self.label.pk})
        )
        self.assertEqual(Label.objects.count(), initial_count)
        
        messages = list(get_messages(resp.wsgi_request))
        self.assertEqual(
            str(messages[0]),
            'Невозможно удалить метку, потому что она используется'
        )

    def test_delete_view_displays_correct_content(self):
        label = self.label.pk
                
        resp = self.client.get(
            reverse(
                'labels:delete',
                kwargs={'pk': label}
                )
            )
        
        expected_message = f'Вы уверены, что хотите удалить {self.label.name}'
        
        self.assertContains(resp, 'method="post"', status_code=200)
        self.assertContains(resp, 'Удаление метки')
        self.assertContains(resp, expected_message)
        self.assertContains(resp, 'type="submit"')
        self.assertContains(resp, 'Да, удалить')
