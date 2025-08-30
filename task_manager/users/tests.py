from django.contrib.auth import get_user_model
from django.contrib.messages import get_messages
from django.test import TestCase
from django.urls import reverse

from task_manager.users.forms import CustomUserCreationForm


User = get_user_model()


class SignUpViewTest(TestCase):
    
    @classmethod
    def setUpTestData(cls):
        cls.valid_data = {
            'username': 'NewUser',
            'first_name': 'New_First_Name',
            'last_name': 'New_last_Name',
            'password1': 'test_password123',
            'password2': 'test_password123',
        }
    
    def test_signup_view_uses_correct_template_form(self):
        resp = self.client.get(reverse('users:create'))
        self.assertTemplateUsed(resp, 'users/create.html')
        self.assertIsInstance(resp.context['form'], CustomUserCreationForm)
        self.assertEqual(resp.status_code, 200)
      
    def test_successful_signup_redirects_to_login(self):
        initial_count = User.objects.count()

        resp = self.client.post(
            reverse('users:create'),
            data=self.valid_data,
        )
        self.assertRedirects(resp, reverse('login'), status_code=302)

        messages = list(get_messages(resp.wsgi_request))
        self.assertEqual(
            str(messages[0]),
            "Пользователь успешно зарегистрирован!"
        )

        self.assertEqual(User.objects.count(), initial_count + 1)
        
        new_user = User.objects.get(username='NewUser') 
        self.assertEqual(new_user.first_name, 'New_First_Name')
        self.assertEqual(new_user.last_name, 'New_last_Name')
        self.assertTrue(new_user.check_password('test_password123'))
        
        self.assertTrue(self.client.login(
            username='NewUser',
            password='test_password123'
            )
        )

    def test_invalid_signup_shows_errors(self):
        invalid_data = {
            'username': '',
            'first_name': '',
            'last_name': '',
            'password1': '123', 
            'password2': '456'
        }
        resp = self.client.post(
        reverse('users:create'),
        data=invalid_data
        )
        
        self.assertEqual(resp.status_code, 200)
        
        form = resp.context['form']
        
        self.assertIn('username', form.errors)
        self.assertIn('first_name', form.errors)
        self.assertIn('last_name', form.errors)
        self.assertIn('password2', form.errors)
        
        self.assertIn('Обязательное поле.', form.errors['username'])
        self.assertIn('Обязательное поле.', form.errors['first_name'])
        self.assertIn('Обязательное поле.', form.errors['last_name'])
        self.assertIn(
            'Введенные пароли не совпадают.',
            form.errors['password2']
        )

    def test_labels_view_displays_correct_content(self):
        resp = self.client.get(reverse('users:create'))
        
        self.assertContains(resp, 'method="post"')

        self.assertContains(resp, 'Регистрация', status_code=200)
        self.assertContains(resp, 'Имя')
        self.assertContains(resp, 'Фамилия')
        self.assertContains(resp, 'Имя пользователя')
        self.assertContains(resp, 'Пароль')
        self.assertContains(resp, 'Подтверждение пароля')
        
        self.assertContains(resp, 'type="submit"')
        self.assertContains(resp, 'Зарегистрировать')


class UsersViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create(
            username='test_username',
        )
        cls.user.set_password('test_password123')
        cls.user.save()

    def test_users_view_uses_correct_template(self):
        User.objects.create(
            username='anotheruser',
            password='testpass123'
        )

        resp = self.client.get(reverse('users:users'))
        self.assertTemplateUsed(resp, 'users/users.html')
        self.assertEqual(len(resp.context['users']), 2)


class UsersUpdateViewTest(TestCase):
    
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create(
            username='test_username',
            first_name='test_name',
            last_name='test_last',
        )

        cls.user.set_password('test_password123')
        cls.user.save()
        
        cls.other_user = User.objects.create(
            username='otheruser',
        )
        cls.other_user.set_password('testpass123') 
        cls.other_user.save()
        
        cls.new_valid_data = {
            'username': 'new_username',
            'first_name': 'new_name',
            'last_name': 'new_last',
            'password1': 'new_test_password123',
            'password2': 'new_test_password123',
            
        }

    def setUp(self):
        self.client.login(
            username='test_username',
            password='test_password123',
        )

    def test_update_view_uses_correct_template_form(self):
        resp = self.client.get(
            reverse('users:update', kwargs={'pk': self.user.pk})
        )
        self.assertTemplateUsed(resp, 'users/update.html')
        self.assertIsInstance(resp.context['form'], CustomUserCreationForm)

    def test_user_can_update_own_profile(self):        
        resp = self.client.post(
            reverse(
                'users:update',
                kwargs={'pk': self.user.pk}),
                data=self.new_valid_data,
            )

        self.assertRedirects(resp, reverse('users:users'))
        self.user.refresh_from_db()
        self.assertEqual(self.user.username, 'new_username')
        self.assertEqual(self.user.first_name, 'new_name')
        self.assertEqual(self.user.last_name, 'new_last')
        self.assertTrue(self.user.check_password('new_test_password123'))
        
        self.assertFalse(self.client.login(
            username='test_username',
            password='test_password123'
            )
        )
        self.assertTrue(self.client.login(
            username='new_username',
            password='new_test_password123'
            )
        )

        messages = list(get_messages(resp.wsgi_request))
        self.assertEqual(str(messages[0]), "Пользователь успешно изменен")

    def test_user_cannot_update_other_profile(self):
        resp = self.client.get(
            reverse('users:update', kwargs={'pk': self.other_user.pk})
        )
        self.assertRedirects(resp, reverse('users:users'))
        
        messages = list(get_messages(resp.wsgi_request))
        self.assertEqual(
            str(messages[0]),
            "У вас нет прав для изменения другого пользователя."
        )

    def test_labels_view_displays_correct_content(self):
        resp = self.client.get(reverse(
            'users:update',
            kwargs={'pk': self.user.pk}
            )
        )
        
        self.assertContains(resp, "method='post'")

        self.assertContains(resp, 'Изменение пользователя', status_code=200)
        self.assertContains(resp, 'Имя')
        self.assertContains(resp, 'test_name')
        self.assertContains(resp, 'Фамилия')
        self.assertContains(resp, 'test_last')
        self.assertContains(resp, 'Имя пользователя')
        self.assertContains(resp, 'test_username')

        self.assertContains(resp, 'Пароль')
        self.assertContains(resp, 'Подтверждение пароля')
        
        self.assertContains(resp, 'type="submit"')
        self.assertContains(resp, 'Изменить')


class UsersDeleteViewTest(TestCase):
    
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create(
            username='test_username',
        )

        cls.user.set_password('test_password123')
        cls.user.save()
        
        cls.other_user = User.objects.create(
            username='otheruser',
        )
        cls.other_user.set_password('testpass123') 
        cls.other_user.save()
        
    def setUp(self):
        self.client.login(
            username='test_username',
            password='test_password123',
        )

    def test_delete_view_uses_correct_template(self):
        resp = self.client.get(
            reverse('users:delete', kwargs={'pk': self.user.pk})
        )
        self.assertTemplateUsed(resp, 'users/delete.html')
        self.assertEqual(resp.status_code, 200)

    def test_user_can_delete_own_profile(self):
        initial_count = User.objects.count()
        resp = self.client.post(
            reverse('users:delete', kwargs={'pk': self.user.pk})
        )
        self.assertRedirects(resp, reverse('users:users'))
        self.assertEqual(User.objects.count(), initial_count - 1)

        messages = list(get_messages(resp.wsgi_request))
        self.assertEqual(str(messages[0]), "Пользователь успешно удален")

    def test_user_cannot_delete_other_profile(self):
        initial_count = User.objects.count()
        resp = self.client.post(
            reverse('users:delete', kwargs={'pk': self.other_user.pk})
        )
        self.assertRedirects(resp, reverse('users:users'))
        self.assertEqual(User.objects.count(), initial_count)
        
        messages = list(get_messages(resp.wsgi_request))
        self.assertEqual(
            str(messages[0]),
            "У вас нет прав для изменения другого пользователя."
        )

    def test_labels_view_displays_correct_content(self):
        resp = self.client.get(reverse(
            'users:delete',
            kwargs={'pk': self.user.pk}
            )
        )
        
        self.assertContains(resp, 'method="post"')

        self.assertContains(resp, 'Удаление', status_code=200)
        
        self.assertContains(resp, 'type="submit"')
        self.assertContains(resp, 'Да, удалить')
