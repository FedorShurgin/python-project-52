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
