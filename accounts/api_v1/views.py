
from accounts.api_v1.serializers import (CreateUserSerializer,
                                         GetOrUpdateUserListSerializer)
from django.contrib.auth.models import User
from rest_framework import generics, status
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response


class GetUserList(generics.ListAPIView):
    """ List all the user"""
    permission_classes = [IsAdminUser]
    queryset = User.objects.all()
    serializer_class = GetOrUpdateUserListSerializer


class CreateUser(generics.CreateAPIView):
    """
    Create new user
    post data:
    {
    "username": "",
    "email": "",
    "password1": "",
    "password2": ""
}
    """
    permission_classes = [IsAdminUser]
    serializer_class = CreateUserSerializer
    queryset = User.objects.all()

    def post(self, request):
        data = request.data
        user = CreateUserSerializer(data=data)
        user.save()
        return Response(status=status.HTTP_200_OK)


class UpdateUser(generics.RetrieveUpdateDestroyAPIView):
    """ Update user details 
    post data:
    {
    "id": 4,
    "username": "sam",
    "email": "sam@gmail.com"
}
    """
    permission_classes = [IsAdminUser]
    queryset = User.objects.all()
    serializer_class = GetOrUpdateUserListSerializer
