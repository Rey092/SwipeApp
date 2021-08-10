from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient

User = get_user_model()


# noinspection DuplicatedCode
class UserRegistrationTestCase(TestCase):
    def test_user_registration(self):
        """User should be successfully created. Response should return new auth_token for User."""
        url = reverse('users:rest_register')
        data = {
            'username': '+380688835762',
            'password1': 'MyAwesomePassword-258',
            'password2': 'MyAwesomePassword-258',
            'email': 'test001@mail.com',
        }

        response = self.client.post(url, data=data)

        self.assertEqual(status.HTTP_201_CREATED, response.status_code)

        key = response.json()['key']
        token = Token.objects.get(key=key)
        user = User.objects.get(username='+380688835762')

        self.assertEqual(token, user.auth_token)


# noinspection DuplicatedCode,PyPep8Naming
class UserLoginTestCase(TestCase):

    def setUp(self):
        user = User.objects.create(
            username="+380629835869",
            email="test002@mail.com"
        )
        user.set_password('HelloWorld-25367')
        user.save()

    def test_user_login(self):
        """User are correctly identified and logged in. Response should return new auth_token for User."""
        url = reverse('users:rest_login')
        data = {
            "username": "+380629835869",
            "password": "HelloWorld-25367",
        }

        response_good = self.client.post(url, data=data)

        self.assertEqual(status.HTTP_200_OK, response_good.status_code)

        key = response_good.json()['key']
        token = Token.objects.get(key=key)
        user = User.objects.get(username='+380629835869')

        self.assertEqual(token, user.auth_token)


# noinspection DuplicatedCode
class UserLogoutTestCase(TestCase):
    def setUp(self):
        user = User.objects.create(
            username="+380622235999",
            email="test003@mail.com"
        )
        user.set_password('Good-Day-25256')
        user.save()

        url = reverse('users:rest_login')
        data = {
            "username": "+380622235999",
            "password": "Good-Day-25256",
        }
        self.client.post(url, data=data)

    def test_user_logout(self):
        """Relation between the Token object and the current User object should be deleted."""
        user = User.objects.get(username='+380622235999')
        token = Token.objects.get(user=user)

        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)

        url = reverse('users:rest_logout')
        client.post(url)

        token = Token.objects.filter(user=user)
        self.assertFalse(token.exists())
