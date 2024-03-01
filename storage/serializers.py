from rest_framework import serializers
from .models import Folder, File
from git.models import FileInfo

class FolderSerializer(serializers.ModelSerializer):
    class Meta:
        model=Folder
        fields=['id','title','inside']
        read_only_fields = ['user']


class FileViewSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True)
    name = serializers.CharField(source='fileInfo.name')
    size = serializers.FloatField(source='fileInfo.size')

    class Meta:
        model = File
        fields = ['name', 'size', 'timestamp', 'inside']

class FileCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model=File
        fields=['fileInfo','inside']
        read_only_fields = ['user']

class FileInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model=FileInfo
        fields=['name','size']
        
class FileSerializer(serializers.ModelSerializer):
    file_info = FileInfoSerializer(source='fileInfo', read_only=True)
    class Meta:
        model = File
        fields = ['id', 'timestamp', 'file_info','inside']
        read_only_fields = ['user','fileInfo']