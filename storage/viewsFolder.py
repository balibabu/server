from rest_framework.decorators import api_view,permission_classes,authentication_classes
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import generics
from .serializers import FolderSerializer, FileViewSerializer, FileSerializer
from .models import Folder, File

class FolderListCreateView(generics.ListCreateAPIView):
    serializer_class=FolderSerializer
    permission_classes=[IsAuthenticated]
    def get_queryset(self):
        return Folder.objects.filter(user=self.request.user)
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class FolderUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class=FolderSerializer
    permission_classes=[IsAuthenticated]
    def get_queryset(self):
        return Folder.objects.filter(user=self.request.user)
    

@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def getFilesAndFolders(request):
    user = request.user
    files=File.objects.filter(user=user).order_by('-timestamp')
    print(len(files))
    file_serializer=FileSerializer(files,many=True)

    folders=Folder.objects.filter(user=user)
    folder_serializer=FolderSerializer(folders,many=True)
    return Response({'files':file_serializer.data,'folders':folder_serializer.data})