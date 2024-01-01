from rest_framework.decorators import api_view,permission_classes,authentication_classes
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.contrib.auth.models import User
from rest_framework import status
from .serializers import StorageSerializer
from .models import Storage
from django.shortcuts import get_object_or_404

@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def getFiles(request):
    user = request.user
    files=Storage.objects.filter(user=user).order_by('-timestamp')
    serializer=StorageSerializer(files,many=True)
    return Response(serializer.data)
    
from .githubManager import GithubManager
file=open('gitToken.env')
token=file.read()
github_manager = GithubManager(token)


@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def uploadFile(request):
    user = request.user
    github_manager.set_folder_name(user.username)
    uploaded_file = request.FILES.get('file')
    upload_url, uploaded_file_name = github_manager.upload_in_memory_file(uploaded_file)
    if(upload_url and uploaded_file_name):
        newFile=Storage.objects.create(user=user,
                                       uploadedName=uploaded_file_name,
                                       originalName=uploaded_file.name,
                                       fileSize=uploaded_file.size/1024, # in KB
                                       url=upload_url)
        newFile.save()
        response_data = {
            'id': newFile.id,
            'uploadedName': newFile.uploadedName,
            'originalName': newFile.originalName,
            'url': newFile.url,
            'timestamp':newFile.timestamp,
            'fileSize':newFile.fileSize,
        }
        return Response(response_data,status=status.HTTP_201_CREATED)
    return Response(status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def deleteFile(request,sid):
    user = request.user
    storage_instance = get_object_or_404(Storage, id=sid, user=user)
    filename = storage_instance.uploadedName
    github_manager.set_folder_name(user.username)
    if github_manager.delete_image_completely(filename):
        storage_instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    else:
        return Response({'error': 'Failed to delete the file.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)