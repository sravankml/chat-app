# Create your tests here.
from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient, APITestCase


class AccountTests(APITestCase):

    def __init__(self, *args, **kwargs):
        self.access_token = None
        super().__init__(*args, **kwargs)

    def setUp(self):

        User.objects.create_user(
            username='admin', password='admin@123', is_superuser=True,
            is_staff=True, is_active=True)
        User.objects.create_user(
            username='sample', password='sample@123', is_active=True)

    def generate_access_token(self):
        url = reverse('token_obtain_pair')
        data = {
            "username": "admin",
            "password": "admin@123"
        }
        response = self.client.post(url, data, format='json')
        print(response.status_code)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        access_token = response.data.get('access')
        return f"JWT {access_token}"

    def test_create_new_member(self):
        """
        Creating new user
        """

        access_token = self.generate_access_token()

        data = {
            "username": "testuser",
            "password1": "test@123",
            "password2": "test@123"
        }

        url = reverse('user-create')
        self.client.credentials(HTTP_AUTHORIZATION=access_token)

        self.client.post(url, data, format='json')

        self.assertEqual(User.objects.filter(username='testuser').count(), 1)

    def test_edit_user(self):
        """
        Edit New Member
        """
        access_token = self.generate_access_token()
        data = {
            "username": "testuser1"
        }

        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION=access_token)

        userid = User.objects.get(username='sample').id

        client.put(
            f'/api/v1/user/update/{userid}/', data, format='json')

        self.assertEqual(User.objects.filter(username='testuser1').count(), 1)
