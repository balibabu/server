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


@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def send_msg_get_latest_msg(request):
    sender = request.user
    rid=request.data.get('receiver_id')
    receiver = User.objects.get(id=rid)
    content=request.data.get('content')
    data={'content':content}
    serializer=MessageSerializer(data=data)
    if serializer.is_valid():
        serializer.save(sender=sender,receiver=receiver)

    last_msg_id=request.data.get('last_msg_id')
    queryset = Message.objects.filter(
        sender=receiver,
        receiver=sender,
        id__gt=last_msg_id
    ).order_by('timestamp')

    serializer2=MessageSerializer(queryset,many=True)
    msgs=serializer2.data
    msgs.append(serializer.data)
    return Response(msgs)