from groups.models import ChatGroup, GroupMemberChat, LikeMessage
from rest_framework import serializers


class ChatGroupSerializer(serializers.ModelSerializer):
    created_at = serializers.DateTimeField(read_only=True)
    modified_at = serializers.DateTimeField(read_only=True)

    class Meta:
        model = ChatGroup
        fields = '__all__'


class GroupMemberChatSerializer(serializers.ModelSerializer):
    class Meta:
        model = GroupMemberChat
        fields = '__all__'


class LikeMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = LikeMessage
        fields = '__all__'
