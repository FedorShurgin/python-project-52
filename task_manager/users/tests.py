from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.messages import get_messages
from task_manager.users.forms import CustomUserCreationForm

class SignUpViewTest(TestCase):
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
            data={
                'username': 'NewUser',
                'first_name': 'New_First_Name',
                'last_name': 'New_last_Name',
                'password1': 'test_password123',
                'password2': 'test_password123'
            }
        )
        self.assertRedirects(resp, reverse('login'), status_code=302)

    def test_successful_signup_shows_message(self):
        resp = self.client.post(
            reverse('users:create'),
            data={
                'username': 'NewUser',
                'first_name': 'New_First_Name',
                'last_name': 'New_last_Name',
                'password1': 'test_password123',
                'password2': 'test_password123'
            }
        )
        messages = list(get_messages(resp.wsgi_request))
        self.assertEqual(str(messages[0]), "Пользователь успешно зарегистрирован!")

    def test_signup_creates_user(self):
        initial_count = User.objects.count()
        resp = self.client.post(
            reverse('users:create'),
            data={
                'username': 'NewUser',
                'first_name': 'New_First_Name',
                'last_name': 'New_last_Name',
                'password1': 'test_password123',
                'password2': 'test_password123'
            }
        )
        self.assertEqual(User.objects.count(), initial_count + 1)
