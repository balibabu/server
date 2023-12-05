from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from rest_framework.authtoken.models import Token
from django.contrib.auth import logout
from django.views.decorators.csrf import csrf_exempt

@api_view(['POST'])
@csrf_exempt
def register_api_view(request):
    username = request.data.get('username')
    password = request.data.get('password')
    email = request.data.get('email')
    if User.objects.filter(username=username).exists():
        return Response({'status': 'error', 'message': 'Username is already taken'}, status=status.HTTP_200_OK)
    User.objects.create_user(username=username, password=password, email=email)
    return Response({'status': 'success', 'message': 'User registered successfully'}, status=status.HTTP_201_CREATED)

@api_view(['POST'])
@csrf_exempt
def login_api_view(request):
    username = request.data.get('username')
    password = request.data.get('password')
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        token, created = Token.objects.get_or_create(user=user)
        return Response({'token': token.key}, status=status.HTTP_200_OK)
    else:
        return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)


@api_view(['POST'])
@csrf_exempt
def logout_api_view(request):
    logout(request)
    return Response({'message': 'User logged out successfully'}, status=status.HTTP_200_OK)
