from accounts.api_v1.views import CreateUser, GetUserList, UpdateUser
from django.urls import path

urlpatterns = [
    path('list/', GetUserList.as_view(), name='user-list'),
    path('create/', CreateUser.as_view(), name='user-create'),
    path('update/<int:pk>/', UpdateUser.as_view(), name='user-update'),
]
