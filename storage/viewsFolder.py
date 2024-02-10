from rest_framework.decorators import api_view,permission_classes,authentication_classes
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework import generics
from .serializers import FolderSerializer
from .models import Folder
from rest_framework.response import Response
from .serializers import StorageSerializer
from .models import Storage

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
    files=Storage.objects.filter(user=user).order_by('-timestamp')
    file_serializer=StorageSerializer(files,many=True)
    folders=Folder.objects.filter(user=user)
    folder_serializer=FolderSerializer(folders,many=True)
    return Response({'files':file_serializer.data,'folders':folder_serializer.data})