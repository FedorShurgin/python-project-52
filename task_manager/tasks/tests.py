from django.contrib.auth.models import User
from django.contrib.messages import get_messages
from django.test import TestCase
from django.urls import reverse

from task_manager.labels.models import LabelsModel
from task_manager.statuses.models import StatusesModel
from task_manager.tasks.forms import TasksCreateForm
from task_manager.tasks.models import TasksModel

class TasksFilterTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user_1 = User.objects.create(
            username='test_username_1',
        )
        cls.user_1.set_password('test_password123')
        cls.user_1.save()

        cls.user_2 = User.objects.create(
            username='test_username_2',
        )
        cls.user_2.set_password('test_1234password')
        cls.user_2.save()
        
        cls.status_1 = StatusesModel.objects.create(name='Test Status 1')
        cls.status_2 = StatusesModel.objects.create(name='Test Status 2')
        cls.label_1 = LabelsModel.objects.create(name='Test Label 1')
        cls.label_2 = LabelsModel.objects.create(name='Test Label 2')
        
        number_of_task = 5
        for task_num in range(number_of_task):
            if task_num % 2 != 0:
                TasksModel.objects.create(
                    name = f'Task {task_num}',
                    author=cls.user_1,
                    status=cls.status_1,
                    executor=cls.user_1,
                ).labels.add(cls.label_1)
            else:
                TasksModel.objects.create(
                    name = f'Task {task_num}',
                    author=cls.user_2,
                    status=cls.status_2,
                    executor=cls.user_2,
                ).labels.add(cls.label_2)
  
    def setUp(self):
        self.client.login(
            username='test_username_1',
            password='test_password123',
        )

    def test_tasks_view_uses_correct_template(self):
        resp = self.client.get(reverse('tasks:tasks'))
        self.assertTemplateUsed(resp, 'tasks/tasks.html')
        self.assertEqual(resp.status_code, 200)
    
    def test_filter_by_status(self):
        resp = self.client.get(
            reverse('tasks:tasks'),
            {'status': self.status_1.pk}
        )
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(len(resp.context['tasks']), 2)
    
    def test_filter_by_label(self):
        resp = self.client.get(
            reverse('tasks:tasks'),
            {'labels': self.label_2.pk}
        )
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(len(resp.context['tasks']), 3)
    
    def test_filter_by_executor(self):
        resp = self.client.get(
            reverse('tasks:tasks'),
            {'executor': self.user_2.pk}
        )
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(len(resp.context['tasks']), 3)
        
    def test_filter_combined(self):
        resp = self.client.get(
            reverse('tasks:tasks'),
            {
                'author': self.user_1.pk,
                'status': self.status_1.pk
            }
        )
        
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(len(resp.context['tasks']), 2)

    # def test_filter_my_tasks(self):
    #     all_tasks_count = TasksModel.objects.count()
        
    #     resp = self.client.get(
    #         reverse('tasks:tasks'),
    #         {'self_tasks': 'on'}
    #     )
    #     self.assertEqual(resp.status_code, 200)
    #     filtered_tasks = resp.context['tasks']
    #     self.assertLess(len(filtered_tasks), all_tasks_count)
        
    #     for task in filtered_tasks:
    #         self.assertEqual(task.author, self.user_1)
        
    #     self.assertEqual(len(filtered_tasks), 2)
        
    #     other_user_tasks = TasksModel.objects.filter(author=self.user_2)
    #     for task in other_user_tasks:
    #         self.assertNotIn(task, filtered_tasks)


class TasksCreateViewTest(TestCase):
    
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create(
            username='test_username',
        )

        cls.user.set_password('test_password123')
        cls.user.save()
        
        cls.status = StatusesModel.objects.create(name='Test Status')
        cls.label = LabelsModel.objects.create(name='Test Label')
        cls.executor = User.objects.create(
            username='executor_user',
        )
        
        cls.valid_data = {
            'name': 'Test Task',
            'description': 'Test Description',
            'status': cls.status.pk,
            'executor': cls.executor.pk,
            'labels': [cls.label.pk],
        }

    def setUp(self):
        self.client.login(
            username='test_username',
            password='test_password123',
        )

    def test_task_view_uses_correct_template(self):
        resp = self.client.get(reverse('tasks:create'))
        self.assertTemplateUsed(resp, 'tasks/create.html')
        self.assertEqual(resp.status_code, 200)

    def test_task_view_uses_correct_form(self):
        resp = self.client.get(reverse('tasks:create'))
        self.assertIsInstance(resp.context['form'], TasksCreateForm)

    def test_task_view_displays_correct_content(self):
        resp = self.client.get(reverse('tasks:create'))
        
        self.assertContains(resp, 'method="post"')

        self.assertContains(resp, 'Создать задачу', status_code=200)
        self.assertContains(resp, 'Имя')
        self.assertContains(resp, 'Описание')
        self.assertContains(resp, 'Статус')
        self.assertContains(resp, 'Исполнитель')
        self.assertContains(resp, 'Метки')

        self.assertContains(resp, 'type="submit"')
        self.assertContains(resp, 'Создать')

    def test_create_task_success(self):
        resp = self.client.post(
            reverse('tasks:create'),
            data=self.valid_data
        )
        self.assertRedirects(resp, reverse('tasks:tasks'))
        
        messages = list(get_messages(resp.wsgi_request))
        self.assertEqual(str(messages[0]), "Задача успешно создана")

    def test_created_task_exists_in_db(self):
        
        self.client.post(
            reverse('tasks:create'),
            data=self.valid_data,
        )
        task = TasksModel.objects.first()
        self.assertEqual(task.name, 'Test Task')
        self.assertEqual(task.author, self.user)
        self.assertEqual(task.status, self.status)
        self.assertEqual(task.executor, self.executor)
        self.assertEqual(list(task.labels.all()), [self.label])


class TasksUpdateViewTest(TestCase):
    
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create(
            username='test_username',
        )
        cls.user.set_password('test_password123')
        cls.user.save()
        
        cls.executor = User.objects.create(
            username='executor_user',
        )
        
        cls.status1 = StatusesModel.objects.create(name='Original Status')
        cls.status2 = StatusesModel.objects.create(name='Updated Status')
        
        cls.label1 = LabelsModel.objects.create(name='Original Label')
        cls.label2 = LabelsModel.objects.create(name='Updated Label')
        
        cls.task = TasksModel.objects.create(
            name='Original Task',
            description='Original Description',
            author=cls.user,
            status=cls.status1,
            executor=cls.executor,
        )
        cls.task.labels.add(cls.label1)
        
        cls.updated_data = {
            'name': 'Updated Task',
            'description': 'Updated Description',
            'status': cls.status2.pk,
            'executor': cls.executor.pk,
            'labels': [cls.label2.pk],
        }

    def setUp(self):
        self.client.login(
            username='test_username',
            password='test_password123',
        )

    def test_task_view_uses_correct_template(self):
        resp = self.client.get(reverse(
            'tasks:update',
            kwargs={'pk': self.task.pk}
            )
        )
        self.assertTemplateUsed(resp, 'tasks/update.html')
        self.assertEqual(resp.status_code, 200)

    def test_update_task_success(self):
        resp = self.client.post(
            reverse('tasks:update', kwargs={'pk': self.task.pk}),
            data=self.updated_data
        )
        self.assertRedirects(resp, reverse('tasks:tasks'))
        self.task.refresh_from_db()
        self.assertEqual(self.task.name, 'Updated Task')
        self.assertEqual(self.task.description, 'Updated Description')
        self.assertEqual(self.task.author, self.user)
        self.assertEqual(self.task.status, self.status2)
        self.assertEqual(self.task.executor, self.executor)
        self.assertEqual(list(self.task.labels.all()), [self.label2])
        
        messages = list(get_messages(resp.wsgi_request))
        self.assertEqual(str(messages[0]), "Задача успешно изменена")

    def test_task_view_displays_correct_content(self):
        resp = self.client.get(reverse(
            'tasks:update',
            kwargs={'pk': self.task.pk}
            )
        )
        
        self.assertContains(resp, "method='post'")

        self.assertContains(resp, 'Изменение задачи', status_code=200)
        self.assertContains(resp, 'Имя')
        self.assertContains(resp, 'Original Task')
        self.assertContains(resp, 'Описание')
        self.assertContains(resp, 'Original Description')
        self.assertContains(resp, 'Статус')
        self.assertContains(resp, 'Original Status')
        self.assertContains(resp, 'Исполнитель')
        self.assertContains(resp, 'Метки')
        self.assertContains(resp, 'Updated Label')

        self.assertContains(resp, 'type="submit"')
        self.assertContains(resp, 'Изменить')


class TaskTaskView(TestCase):
    
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create(
            username='test_username',
        )

        cls.user.set_password('test_password123')
        cls.user.save()
        
        cls.status = StatusesModel.objects.create(name='Test Status')
        cls.label = LabelsModel.objects.create(name='Test Label')
        cls.executor = User.objects.create(
            username='executor_user',
        )
        
        cls.task = TasksModel.objects.create(
            name='Test Task',
            description='Test Description',
            author=cls.user,
            status=cls.status,
            executor=cls.executor,
        )
        cls.task.labels.add(cls.label)

    def setUp(self):
        self.client.login(
            username='test_username',
            password='test_password123',
        )

    def test_task_view_uses_correct_template(self):
        resp = self.client.get(reverse(
            'tasks:task',
            kwargs={'pk': self.task.pk}
            )
        )
        self.assertTemplateUsed(resp, 'tasks/task.html')
        self.assertEqual(resp.status_code, 200)

    def test_task_view_displays_correct_content(self):
        resp = self.client.get(reverse(
            'tasks:task',
            kwargs={'pk': self.task.pk}
            )
        )
        
        self.assertContains(resp, 'Просмотр задачи', status_code=200)
        self.assertContains(resp, 'Задача')
        self.assertContains(resp, 'Описание')
        self.assertContains(resp, 'Статус')
        self.assertContains(resp, 'Дата создания')
        self.assertContains(resp, 'Исполнитель')
        self.assertContains(resp, 'Метки')


class TasksDeleteViewTest(TestCase):
    
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create(
            username='test_username',
        )

        cls.user.set_password('test_password123')
        cls.user.save()
        
        cls.status = StatusesModel.objects.create(name='Test Status')
        cls.label = LabelsModel.objects.create(name='Test Label')
        cls.executor = User.objects.create(
            username='executor_user',
        )
        cls.author = User.objects.create(
            username='test_author',
        )
        
        cls.task = TasksModel.objects.create(
            name='Test Task',
            description='Test Description',
            author=cls.user,
            status=cls.status,
            executor=cls.executor,
        )
        cls.task.labels.add(cls.label)

    def setUp(self):
        self.client.login(
            username='test_username',
            password='test_password123',
        )
    
    def test_delete_view_uses_correct_template(self):
        resp = self.client.get(
            reverse('tasks:delete', kwargs={'pk': self.task.pk})
        )
        self.assertTemplateUsed(resp, 'tasks/delete.html')
        self.assertEqual(resp.status_code, 200)

    def test_delete_task_success(self):
        resp = self.client.post(
            reverse('tasks:delete', kwargs={'pk': self.task.pk})
        )
        self.assertRedirects(resp, reverse('tasks:tasks'))
        
        messages = list(get_messages(resp.wsgi_request))
        self.assertEqual(str(messages[0]), "Задача успешно удалена")
    
    def test_task_view_displays_correct_content(self):
        resp = self.client.get(reverse(
            'tasks:delete',
            kwargs={'pk': self.task.pk}
            )
        )
        
        self.assertContains(resp, 'method="post"')

        self.assertContains(resp, 'Удаление', status_code=200)

        self.assertContains(resp, 'type="submit"')
        self.assertContains(resp, 'Да, удалить')

    def test_cannot_delete_used_task(self):
        task = TasksModel.objects.create(
            name='Test Task',
            description='Test Description',
            author=self.author,
            status=self.status,
            executor=self.executor,
        )
        task.labels.add(self.label)
        
        initial_count = TasksModel.objects.count()
        resp = self.client.post(
            reverse('tasks:delete', kwargs={'pk': task.pk})
        )
        self.assertEqual(TasksModel.objects.count(), initial_count)
        self.assertRedirects(resp, reverse('tasks:tasks'))

        messages = list(get_messages(resp.wsgi_request))
        self.assertEqual(
            str(messages[0]),
            'Задачу может удалить только ее автор'
        )

    def test_task_view_displays_correct_content(self):
        resp = self.client.get(reverse(
            'tasks:delete',
            kwargs={'pk': self.task.pk}
            )
        )
        
        self.assertContains(resp, 'method="post"')

        self.assertContains(resp, 'Удаление')

        self.assertContains(resp, 'type="submit"')
        self.assertContains(resp, 'Да, удалить')
