from rest_framework.decorators import api_view,permission_classes,authentication_classes
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.contrib.auth.models import User
from rest_framework import status
from django.db.models import Q
from rest_framework import generics, permissions, status


@api_view(['GET'])
def greet(request):
    return Response("Hello",status=status.HTTP_200_OK)