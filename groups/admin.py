from django.contrib import admin

# Register your models here.
from groups.models import ChatGroup, GroupMemberChat

admin.site.register(ChatGroup)
admin.site.register(GroupMemberChat)
