from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.messages import get_messages
from task_manager.users.forms import CustomUserCreationForm

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
    
    def test_signup_view_uses_correct_template(self):
        resp = self.client.get(reverse('users:create'))
        self.assertTemplateUsed(resp, 'users/create.html')
        self.assertEqual(resp.status_code, 200)


    def test_signup_view_uses_correct_form(self):
        resp = self.client.get(reverse('users:create'))
        self.assertIsInstance(resp.context['form'], CustomUserCreationForm)
        
    def test_successful_signup_redirects_to_login(self):
        resp = self.client.post(
            reverse('users:create'),
            data=self.valid_data,
        )
        self.assertRedirects(resp, reverse('login'), status_code=302)

    def test_successful_signup_shows_message(self):
        resp = self.client.post(
            reverse('users:create'),
            data=self.valid_data,
        )
        messages = list(get_messages(resp.wsgi_request))
        self.assertEqual(str(messages[0]), "Пользователь успешно зарегистрирован!")

    def test_signup_creates_user(self):
        initial_count = User.objects.count()
        resp = self.client.post(
            reverse('users:create'),
            data=self.valid_data,
        )
        self.assertEqual(User.objects.count(), initial_count + 1)

class UsersViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create(
            username='test_username',
        )
        cls.user.set_password('test_password123')
        cls.user.save()

    def test_users_view_uses_correct_template(self):
        resp = self.client.get(reverse('users:users'))
        self.assertTemplateUsed(resp, 'users/users.html')

    def test_users_view_shows_all_users(self):
        User.objects.create(username='anotheruser', password='testpass123')
        response = self.client.get(reverse('users:users'))
        self.assertEqual(len(response.context['users']), 2)

class UsersUpdateViewTest(TestCase):
    
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create(
            username='test_username',
            first_name = 'test_name',
            last_name ='test_last',
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

    def test_update_view_uses_correct_template(self):
        resp = self.client.get(
            reverse('users:update', kwargs={'pk': self.user.pk})
        )
        self.assertTemplateUsed(resp, 'users/update.html')

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
        
        self.assertFalse(self.client.login(username='test_username', password='test_password123'))
        self.assertTrue(self.client.login(username='new_username', password='new_test_password123'))

    def test_update_shows_success_message(self):
        resp = self.client.post(
            reverse('users:update', kwargs={'pk': self.user.pk}), data=self.new_valid_data)
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
