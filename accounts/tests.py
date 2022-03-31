# Create your tests here.
from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, RequestsClient


class AccountTests(APITestCase):

    def setUp(self):

        User.objects.create_user(
            username='admin', password='admin@123', is_superuser=True,
            is_staff=True, is_active=True)

    def test_create_account(self):
        """
        Ensure we can create a new account object.
        """

        self.assertEqual(User.objects.count(), 1)

        url = reverse('token_obtain_pair')
        data = {
            "username": "admin",
            "password": "admin@123"
        }
        response = self.client.post(url, data, format='json')
        print(response.status_code)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        access_token = response.data.get('access')

        headers = {
            "authorization": f"JWT {access_token}"
        }
        client = RequestsClient()
        response = client.post('http://127.0.0.1:8000/api/v1/user/create/',
                               json={
                                   "username": "testuser",
                                   "password1": "test@123",
                                   "password2": "test@123"
                               }, headers=headers)
