from django.urls import path
from .views import MessageListView, UserListView, ReceivedMessageListView, SendMessageView, DeleteMessageView,LatestMessageView

urlpatterns = [
    path('users/', UserListView.as_view(), name='user-list'),
    path('received-messages/', ReceivedMessageListView.as_view(), name='received-messages-list'),
    path('latest-messages/', LatestMessageView.as_view(), name='latest-messages-list'),
    path('send-message/', SendMessageView.as_view(), name='send-message'),
    path('messages/<int:userid>/', MessageListView.as_view(), name='message-list'),

    # path('delete-message/<int:pk>/', DeleteMessageView.as_view(), name='delete-message'), # delete own msg only
]