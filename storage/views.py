from rest_framework.decorators import api_view,permission_classes,authentication_classes
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.http import HttpResponse
from rest_framework import status
from .serializers import FileViewSerializer,FileSerializer
from .models import File
from git.extra.config import MAX_GIT_FILE_SIZE
from git.extra.fileManager import FileManager
from .utility.chunkManager import ChunkManagerForStorage

chunkStore={}

@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def uploadFile(request):
    user = request.user
    file = request.FILES.get('file')
    key=(user.username,request.data.get('fileKey'))
    if not file:
        obj=ChunkManagerForStorage(request.data)
        chunkStore[key]=obj
        return Response({'max-chunk-size':MAX_GIT_FILE_SIZE})
    else:
        chunkStore[key].add_chunk(request.data,file)
    
    obj=chunkStore[key]
    if obj.is_completed():
        chunks=obj.get_chunks()
        fm=FileManager(user.username)
        fileInfo=fm.upload(chunks,obj.filename)
        serializer = FileSerializer(data={'inside':obj.inside})
        if serializer.is_valid():
            serializer.save(user=user,fileInfo=fileInfo)
            del chunkStore[key]
            return Response(serializer.data)
        else:
            fm.delete(fileInfo)
            return Response(serializer.errors)
    return Response('chunk received')

@api_view(['DELETE'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def deleteFile(request,file_id):
    user = request.user
    file=File.objects.get(id=file_id)
    fm=FileManager(user.username)
    fm.delete(file.fileInfo)
    return Response(status=status.HTTP_204_NO_CONTENT)
    
@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def downloadFile(request,file_id):
    user = request.user
    fm=FileManager(user.username)
    file=File.objects.get(id=file_id)
    file_content=fm.download(file.fileInfo)
    if not file_content: return Response({'error':'something went wrong'},status=400)
    response = HttpResponse(file_content, content_type='application/octet-stream')
    response['Content-Disposition'] = file.fileInfo.name
    response['Access-Control-Expose-Headers'] = 'Content-Disposition'
    return response

from rest_framework import generics
class UpdateFileView(generics.UpdateAPIView):
    serializer_class=FileSerializer
    permission_classes=[IsAuthenticated]
    def get_queryset(self):
        return File.objects.filter(user=self.request.user)