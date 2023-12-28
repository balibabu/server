from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.contrib.auth.models import User
from chat.models import Message
from chat.serializers import MessageSerializer

@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def get_new_messages(request, msgid, senderid):
    user = request.user
    sender=User.objects.get(pk=senderid)
    queryset = Message.objects.filter(
        sender=sender,
        receiver=user,
        id__gt=msgid
    ).order_by('timestamp')

    serializer = MessageSerializer(queryset, many=True)
    return Response(serializer.data)
