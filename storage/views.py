from rest_framework.decorators import api_view,permission_classes,authentication_classes
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from .utils.repoSizeHandler import RepoSizeHandler
from django.shortcuts import get_object_or_404
from .utils.githubManager import GithubManager
from rest_framework.response import Response
from .serializers import StorageSerializer
from .models import Storage, GithubInfo
from django.http import HttpResponse
from rest_framework import status

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
    token = request.data.get('token', str(tk))
    repoHandler=RepoSizeHandler(token,user.username)
    repo_name=repoHandler.get_free_repo(repo_owner)
    github_info, created = GithubInfo.objects.get_or_create( repo_owner=repo_owner,repo_name=repo_name,token=token)
    status,uploaded_filename = repoHandler.upload_file(repo_owner,repo_name,file)
    if not status: return Response({'errors':uploaded_filename},status=404)

    data = {
        'originalName': file.name,
        'fileSize': file.size,
        'uploadedName':uploaded_filename
    }

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
    obj=RepoSizeHandler(token,user.username)
    if obj.delete_file(repo_owner,repo_name,file.uploadedName,file.fileSize):
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
    file_name = storage.uploadedName

    github_info = storage.github
    token = github_info.token
    repo_owner = github_info.repo_owner
    repo_name = github_info.repo_name

    github_manager = GithubManager(token, user.username)
    status, file_content = github_manager.get_file_content(repo_owner,repo_name,file_name)
    if not status: return Response({'error':file_content},status=400)
    response = HttpResponse(file_content, content_type='application/octet-stream')
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