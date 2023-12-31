from rest_framework import serializers
from .models import Storage, GithubInfo

class GithubInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = GithubInfo
        fields = ['repo_owner', 'repo_name']

class StorageSerializer(serializers.ModelSerializer):
    github_info = GithubInfoSerializer(source='github', read_only=True)
    class Meta:
        model = Storage
        fields = ['id', 'uploadedName', 'originalName', 'fileSize', 'timestamp', 'github_info']
        read_only_fields = ['user', 'github']