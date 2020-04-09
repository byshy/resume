from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase
from rest_framework import status

from .models import User


class HomeListViewTestCase(APITestCase):
    list_projects_url = reverse("api_home:all_projects")

    def test_get_all_projects(self):
        response = self.client.get(self.list_projects_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class HomeAPIViewTestCase(APITestCase):
    create_project_url = reverse("api_home:create_project")

    data = {"title": "test title", "content": "test content", "githubURL": "asd", "imageURL": "asd",
            "tags": "tags", "pub_date": "2020-04-02T04:31:00+03:00"}

    def setUp(self):
        self.user = User.objects.create_user(email="email@example.com",
                                             password="some pass",
                                             username="n")
        self.token = Token.objects.create(user=self.user)
        self.api_auth()

    def api_auth(self):
        self.client.login(email="email@example.com", password="some pass")

    def test_create_project_logged_in(self):
        response = self.client.post(self.create_project_url, self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_project_not_logged_in(self):
        self.client.logout()
        response = self.client.post(self.create_project_url, self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class HomeRUDViewTestCase(APITestCase):
    get_project_url = reverse("api_home:get_project", kwargs={'id': 1})

    def setUp(self):
        self.user = User.objects.create_user(email="email@example.com",
                                             password="some pass",
                                             username="n")
        self.token = Token.objects.create(user=self.user)
        self.api_auth()

    def api_auth(self):
        self.client.login(email="email@example.com", password="some pass")

    def test_get_project_logged_in(self):
        response = self.client.get(self.get_project_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_project_not_logged_in(self):
        self.client.logout()
        response = self.client.get(self.get_project_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class GetAllUsersViewSetTestCase(APITestCase):
    list_users_url = reverse("api_home:all_users")

    def setUp(self):
        # had to be super user to get the full list of users
        self.user = User.objects.create_superuser(email="email@example.com", password="some pass", username="n")
        self.token = Token.objects.create(user=self.user)
        self.api_auth()

    def api_auth(self):
        self.client.force_authenticate(self.user, self.token)

    def test_user_list_authenticated(self):
        response = self.client.get(self.list_users_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_list_unauthenticated(self):
        self.client.force_authenticate(user=None)
        response = self.client.get(self.list_users_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class CreateUserViewSetTestCase(APITestCase):
    create_user_url = reverse("api_home:create_user")

    def test_registration(self):
        data = {"email": "email@example.com", "first_name": "first name", "last_name": "last name",
                "password": "some pass", "profile": {"mobile": "123456789"}}
        response = self.client.post(self.create_user_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_registration_not_complete(self):
        data = {"email": "email@example.com", "first_name": "first name", "last_name": "last name",
                "password": "some pass", "profile": {"mobile": ""}}
        response = self.client.post(self.create_user_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class GetUserViewSetTestCase(APITestCase):
    get_user_url = reverse("api_home:get_user", kwargs={'pk': 1})
    fail_get_user_url = reverse("api_home:get_user", kwargs={'pk': 4})

    def setUp(self):
        # had to be super user to get the full list of users
        self.super_user = User.objects.create_superuser(email="super_user@example.com",
                                                        password="some pass",
                                                        username="n")
        self.user = User.objects.create_user(email="email@example.com",
                                             password="some pass",
                                             username="n")
        self.super_token = Token.objects.create(user=self.super_user)
        self.api_auth()

    def api_auth(self):
        self.client.force_authenticate(self.super_user, self.super_token)

    def test_get_user_authenticated(self):
        response = self.client.get(self.get_user_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_no_user_found(self):
        response = self.client.get(self.fail_get_user_url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_get_user_unauthenticated(self):
        self.client.force_authenticate(user=None)
        response = self.client.get(self.get_user_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
