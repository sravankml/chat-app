from accounts.api_v1.serializers import GetOrUpdateUserListSerializer
from django.contrib.auth.models import User
from groups.api_v1.serializers import (ChatGroupSerializer,
                                       GroupMemberChatSerializer,
                                       LikeMessageSerializer)
from groups.models import ChatGroup, GroupMemberChat, LikeMessage
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView


class CreateChatGroup(generics.CreateAPIView):
    """
    API to create new chat group
    post data:
    {
    "name": "new group",
    "members": [1,2]
}
    """
    serializer_class = ChatGroupSerializer
    queryset = ChatGroup.objects.all()


class ListChatGroup(generics.ListAPIView):
    """
    API to to list all the chat group
    """
    serializer_class = ChatGroupSerializer
    queryset = ChatGroup.objects.all()


class UpdateOrDeleteChatGroup(generics.RetrieveUpdateDestroyAPIView):
    """
    API Update or delete chat group
    """
    queryset = ChatGroup.objects.all()
    serializer_class = ChatGroupSerializer


class AddMembers(APIView):

    def get(self, request):
        group_list = ChatGroup.objects.all()
        serialized_group = ChatGroupSerializer(group_list, many=True).data
        member_list = User.objects.all()
        serialized_members = GetOrUpdateUserListSerializer(
            member_list, many=True).data
        return Response({'groups': serialized_group,
                         "members": serialized_members})

    def post(self, request):
        """
        Add members to the chat group
        post data:
        {
        "group_id":1,
        "user_id":[1,2,3]
        }
        """
        data = request.data
        group_id = data.get('group_id')
        user_ids = data.get('user_id')
        get_members = User.objects.filter(id__in=user_ids)
        group = ChatGroup.objects.get(id=group_id)
        group.members.add(*get_members)
        return Response(status=status.HTTP_200_OK)


class SearchChatGroup(APIView):
    """
    API to search chat group
    search:QueryParam: keyword to search
    """

    def get(self, request):
        data = request.GET
        keyword = data.get('search', '')
        group_list = ChatGroup.objects.filter(name__icontains=keyword)
        serialized_group = ChatGroupSerializer(group_list, many=True).data
        return Response(serialized_group)


class SendGroupChat(generics.CreateAPIView):
    """
    Send messages to the chat group
    POST parameter:
    {
    "message": "",
    "chat_group": 1,
    "member": 1
}
    """
    serializer_class = GroupMemberChatSerializer
    queryset = GroupMemberChat.objects.all()


class ListMembersGroupChats(generics.ListAPIView):
    """List all the messages from a group.
    group_id:QueryParam: id of ChatGroup table
     """
    serializer_class = GroupMemberChatSerializer

    def get_queryset(self):
        data = self.request.query_params
        group_id = data.get('group_id')
        return GroupMemberChat.objects.filter(chat_group_id=group_id
                                              ).order_by('created_at')


class MessageLikes(APIView):

    def get(self, request):
        member_chat = LikeMessage.objects.all()
        serialized_member_chat = LikeMessageSerializer(
            member_chat, many=True).data
        return Response(serialized_member_chat)

    def post(self, request):
        """
        Like A chat message
        post data:
       {"message_id":"1"}
        """
        data = request.data
        message_id = data.get('message_id')
        user = request.user

        try:
            like_message = LikeMessage.objects.get(message__id=message_id)
            like_message.liked_by.add(user)
        except LikeMessage.DoesNotExist:
            message = GroupMemberChat.objects.get(id=message_id)
            message_liked = LikeMessage.objects.create(message=message)
            message_liked.liked_by.add(user)
        return Response(status=status.HTTP_200_OK)
