from rest_framework.decorators import api_view,permission_classes,authentication_classes
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.contrib.auth.models import User
from .serializers import MessageSerializer, UserSerializer
from .models import Message, Conversation
from rest_framework import status
from django.db.models import Q
from rest_framework import generics, permissions, status

class UserListView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def send_message(request,userid):
    sender = request.user
    receiver = User.objects.get(id=userid)
    serializer=MessageSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(sender=sender,receiver=receiver)
        return Response(serializer.data,status=status.HTTP_201_CREATED)
    return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def user_conversations(request):
    user = request.user
    user_conversations = Conversation.objects.filter(Q(user1=user) | Q(user2=user))
    latest_messages = Message.objects.filter(id__in=user_conversations.values('last_message')).order_by('-timestamp')
    serializer = MessageSerializer(latest_messages, many=True)
    return Response(serializer.data)

@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def full_conversation(request, userid):
    sender = request.user
    receiver = User.objects.get(pk=userid)
    queryset = Message.objects.filter(
        (Q(sender=sender, receiver=receiver) | Q(sender=receiver, receiver=sender))
    ).order_by('timestamp')
    serializer = MessageSerializer(queryset, many=True)
    return Response(serializer.data)

