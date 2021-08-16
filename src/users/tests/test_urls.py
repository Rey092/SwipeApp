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
        url = reverse("users:rest_register")
        data = {
            "email": "test001@mail.com",
            "password1": "MyAwesomePassword-258",
            "password2": "MyAwesomePassword-258",
            "first_name": "Jhon",
            "last_name": "Black",
        }

        response = self.client.post(url, data=data)

        self.assertEqual(status.HTTP_201_CREATED, response.status_code)

        key = response.json()["key"]
        token = Token.objects.get(key=key)
        user = User.objects.get(email="test001@mail.com")

        self.assertEqual(token, user.auth_token)


# noinspection DuplicatedCode,PyPep8Naming
class UserLoginTestCase(TestCase):
    def setUp(self):
        user = User.objects.create(
            email="test002@mail.com", first_name="Hanna", last_name="Bush"
        )
        user.set_password("HelloWorld-25367")
        user.save()

    def test_user_login(self):
        """User are correctly identified and logged in. Response should return new auth_token for User."""
        url = reverse("users:rest_login")
        data = {
            "email": "test002@mail.com",
            "password": "HelloWorld-25367",
        }

        response_good = self.client.post(url, data=data)

        self.assertEqual(status.HTTP_200_OK, response_good.status_code)

        key = response_good.json()["key"]
        token = Token.objects.get(key=key)
        user = User.objects.get(email="test002@mail.com")

        self.assertEqual(token, user.auth_token)


# noinspection DuplicatedCode
class UserLogoutTestCase(TestCase):
    def setUp(self):
        user = User.objects.create(
            email="test003@mail.com",
            first_name="test_first_name",
            last_name="test_last_name",
        )
        user.set_password("Good-Day-25256")
        user.save()

        url = reverse("users:rest_login")
        data = {
            "email": "test003@mail.com",
            "password": "Good-Day-25256",
        }
        self.client.post(url, data=data)

    def test_user_logout(self):
        """Relation between the Token object and the current User object should be deleted."""
        user = User.objects.get(email="test003@mail.com")
        token = Token.objects.get(user=user)

        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION="Token " + token.key)

        url = reverse("users:rest_logout")
        client.post(url)

        token = Token.objects.filter(user=user)
        self.assertFalse(token.exists())
