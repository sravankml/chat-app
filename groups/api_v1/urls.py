from django.urls import path
from groups.api_v1.views import (AddMembers, CreateChatGroup, ListChatGroup,
                                 ListMembersGroupChats, MessageLikes,
                                 SearchChatGroup, SendGroupChat,
                                 UpdateOrDeleteChatGroup)

urlpatterns = [
    path('create/', CreateChatGroup.as_view(), name='group-create'),
    path('list/', ListChatGroup.as_view(), name='group-list'),
    path('update/delete/<int:pk>/', UpdateOrDeleteChatGroup.as_view(),
         name='group-update-delete'),
    path('add/members/', AddMembers.as_view(), name='group-add-members'),
    path('search/', SearchChatGroup.as_view(), name='search-group'),
    path('chat/send/', SendGroupChat.as_view(), name='send-chat'),
    path('chat/list/', ListMembersGroupChats.as_view(), name='chat-list'),
    path('message/like/', MessageLikes.as_view(), name='message-like')
]
