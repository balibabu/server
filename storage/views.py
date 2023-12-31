from rest_framework.decorators import api_view,permission_classes,authentication_classes
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .serializers import StorageSerializer
from .models import Storage, GithubInfo
from django.shortcuts import get_object_or_404
from django.http import HttpResponse

from .githubManager import GithubManager
file=open('gitToken.env')
tk=file.read()

@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def getFiles(request):
    user = request.user
    files=Storage.objects.filter(user=user).order_by('-timestamp')
    serializer=StorageSerializer(files,many=True)
    return Response(serializer.data)
    
@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def uploadFile(request):
    user = request.user
    file = request.FILES.get('file')
    repo_owner = request.data.get('repo_owner', 'storeage')
    repo_name = request.data.get('repo_name', 'media')
    token = request.data.get('token', str(tk))

    github_info, created = GithubInfo.objects.get_or_create(
        repo_owner=repo_owner,
        repo_name=repo_name,
        token=token
    )
    
    data = {
        'originalName': file.name,
        'fileSize': file.size,
    }
    github_manager = GithubManager(token,repo_owner,repo_name,user.username)
    uploaded_filename = github_manager.upload_in_memory_file(file)
    if not uploaded_filename: return Response(status=404)
    data['uploadedName']=uploaded_filename

    serializer = StorageSerializer(data=data)
    if serializer.is_valid():
        serializer.save(user=user,github=github_info)
        return Response(serializer.data)
    else:
        return Response(serializer.errors)
    

@api_view(['DELETE'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def deleteFile(request,sid):
    user = request.user
    file = get_object_or_404(Storage, id=sid, user=user)
    repo_owner=file.github.repo_owner
    repo_name=file.github.repo_name
    token=file.github.token
    github_manager = GithubManager(token,repo_owner,repo_name,user.username)
    if github_manager.delete_image_completely(file.uploadedName):
        file.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    else:
        return Response({'error': 'Failed to delete the file.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    


@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def downloadFile(request,file_id):
    user = request.user
    storage = Storage.objects.get(id=file_id, user=user)

    # Fetch GitHub information from the database
    github_info = storage.github
    token = github_info.token
    repo_owner = github_info.repo_owner
    repo_name = github_info.repo_name

    # Fetch file details from the Storage object
    file_name = storage.uploadedName
    file_path_in_repo = f"{user.username}/{file_name}"  # Adjust the path accordingly

    # Use GithubManager to get the file content
    github_manager = GithubManager(token, repo_owner, repo_name, user.username)
    file_content = github_manager.get_file_content(file_path_in_repo)

    # Return the file as a response
    response = HttpResponse(file_content, content_type='application/octet-stream')
    response['Content-Disposition'] = f'attachment; filename="{file_name}"'
    return response




from rest_framework import serializers
class GithubInfoCustomSerializer(serializers.ModelSerializer):
    class Meta:
        model = GithubInfo
        fields = ['repo_owner', 'repo_name', 'token']

@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def getGitInfo(request):
    user = request.user
    github_info_list = GithubInfo.objects.filter(storage__user=user).exclude(repo_owner='storeage').distinct()
    # github_info_list = GithubInfo.objects.filter(storage__user=user).distinct()
    serializer = GithubInfoCustomSerializer(github_info_list, many=True)
    return Response(serializer.data)