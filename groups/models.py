from django.db import models
from base.models import AbstractModel
from django.contrib.auth.models import User
# Create your models here.


class ChatGroup(AbstractModel):
    name = models.CharField(max_length=100)
    members = models.ManyToManyField(User)

    def __str__(self):
        return self.name


class GroupMemberChat(AbstractModel):
    chat_group = models.ForeignKey(
        to='groups.ChatGroup', on_delete=models.CASCADE)
    message = models.TextField()
    member = models.ForeignKey(to=User, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.member}-{self.message}'
