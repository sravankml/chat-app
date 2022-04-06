from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from groups.models import ChatGroup, GroupMemberChat


class AccountTests(APITestCase):

    def setUp(self):
        User.objects.create_user(
            username='sample', password='sample@123', is_active=True)
        member = User.objects.create_user(
            username='testuser', password='test@123', is_active=True)
        group = ChatGroup.objects.create(name='sample group')
        GroupMemberChat.objects.create(
            chat_group=group, member=member, message='hello')

    def generate_access_token(self):
        url = reverse('token_obtain_pair')
        data = {
            "username": "sample",
            "password": "sample@123"
        }

        response = self.client.post(url, data, format='json')
        print(response.status_code)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        access_token = response.data.get('access')
        return f"JWT {access_token}"

    def test_create_new_group(self):
        access_token = self.generate_access_token()
        members = User.objects.get(username='sample').id
        data = {
            "name": "new group",
            "members": [members]
        }

        url = reverse('group-create')
        self.client.credentials(HTTP_AUTHORIZATION=access_token)

        self.client.post(url, data, format='json')
        self.assertEqual(ChatGroup.objects.filter(name='new group').count(), 1)

    def test_search_groups(self):
        access_token = self.generate_access_token()

        self.client.credentials(HTTP_AUTHORIZATION=access_token)
        url = reverse('search-group')

        data = {
            'search': 'sample group'
        }
        result = self.client.get(url, data, format='json')

        group_name = result.data[0].get('name')
        self.assertEqual(group_name, 'sample group')

    def test_add_members_to_group(self):
        access_token = self.generate_access_token()
        group_id = ChatGroup.objects.get(name='sample group').id
        members = User.objects.values_list('id', flat=True)
        self.client.credentials(HTTP_AUTHORIZATION=access_token)
        url = reverse('group-add-members')
        data = {
            "group_id": group_id,
            "user_id": members
        }

        self.client.post(url, data, format='json')
        group = ChatGroup.objects.get(name='sample group')
        members = group.members.all().count()
        self.assertEqual(members, 2)

    def test_sent_message_in_group(self):
        access_token = self.generate_access_token()
        group_id = ChatGroup.objects.get(name='sample group')
        members = User.objects.get(username='sample').id
        self.client.credentials(HTTP_AUTHORIZATION=access_token)
        url = reverse('send-chat')
        data = {
            "chat_group": group_id.id,
            "member": members,
            "message": "Hello",
        }

        result = self.client.post(url, data, format='json')
        message = result.data.get('message')
        self.assertEqual(message, 'Hello')

    def test_like_message(self):
        access_token = self.generate_access_token()
        message = GroupMemberChat.objects.get(message='hello')
        self.client.credentials(HTTP_AUTHORIZATION=access_token)
        url = reverse('message-like')
        data = {"message_id": message.id}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
