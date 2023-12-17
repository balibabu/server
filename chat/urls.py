from django.urls import path
from .views import UserListView, ReceivedMessageListView, SendMessageView, DeleteMessageView

urlpatterns = [
    path('users/', UserListView.as_view(), name='user-list'),
    path('received-messages/', ReceivedMessageListView.as_view(), name='received-messages-list'),
    path('send-message/', SendMessageView.as_view(), name='send-message'),
    path('delete-message/<int:pk>/', DeleteMessageView.as_view(), name='delete-message'),
]