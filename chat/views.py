from .serializers import MessageSerializer, UserSerializer
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from django.contrib.auth.models import User
from django.db import models
from .models import Message

class UserListView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

class ReceivedMessageListView(generics.ListAPIView):
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Message.objects.filter(receiver=user)

class SendMessageView(generics.CreateAPIView):
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        receiver_id = self.request.data.get('receiver_id')
        serializer.save(sender=self.request.user, receiver_id=receiver_id)

class DeleteMessageView(generics.DestroyAPIView):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated]


class MessageListView(generics.ListAPIView):
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        sender = self.request.user
        receiver_id = self.kwargs['userid']

        receiver = User.objects.get(pk=receiver_id)

        queryset = Message.objects.filter(
            (models.Q(sender=sender, receiver=receiver) | models.Q(sender=receiver, receiver=sender))
        ).order_by('timestamp')

        return queryset