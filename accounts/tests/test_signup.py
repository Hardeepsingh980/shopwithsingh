from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User


class TestSignUp(TestCase):

    def setUp(self):
        self.username = 'testuser'
        self.password = 'password'

    def test_signup_page_url(self):
        response = self.client.get("/accounts/signup/")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, template_name='accounts/signup.html')

    def test_signup_page_view_name(self):
        response = self.client.get(reverse('signup'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, template_name='accounts/signup.html')

    def test_signup_form(self):
        response = self.client.post(reverse('signup'), data={
            'username': self.username,
            'password1': self.password,
            'password2': self.password
        })
        self.assertEqual(response.status_code, 302)

        users = User.objects.all()
        self.assertEqual(users.count(), 1)
        self.client.login(username=self.username, password=self.password)
