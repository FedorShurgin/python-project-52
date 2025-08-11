# from django.test import TestCase

# from django.contrib.auth.models import User
# from django.urls import reverse


# class UsersViewTest(TestCase):
    
#     @classmethod
#     def setUpTestData(cls):
#         number_of_user = 12
#         for author_num in range(number_of_user):
#             User.objects.create(
#                 first_name='Name %s' % author_num,
#                 last_name ='Surname %s' % author_num,
#                 username='username %s' % author_num,
#                 password = 'test_passwor %s' % author_num,
#             )
    
#     def test_view_url_exists_at_desired_location(self):
#         resp = self.client.get('/users/')
#         self.assertEqual(resp.status_code, 200)
        

#     def test_view_uses_correct_template(self):
#         resp = self.client.get(reverse('users'))
#         self.assertEqual(resp.status_code, 200)
