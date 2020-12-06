from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User


class TestLogin(TestCase):
    def setUp(self):
        self.username = 'testuser'
        self.password = 'password'
        User.objects.create_user(self.username, password=self.password)

    def test_login_page_url(self):
        response = self.client.get("/accounts/login/")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, template_name='accounts/login.html')

    def test_login_page_view_name(self):
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, template_name='accounts/login.html')

    def test_login_form(self):
        response = self.client.post(reverse('login'), data={
            'username': self.username,
            'password': self.password,
        })
        self.assertEqual(response.status_code, 302)

        self.assertEqual(User.objects.get(username=self.username), User.objects.get(pk=self.client.session['_auth_user_id']))
