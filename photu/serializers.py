from rest_framework import serializers
from .models import Photo, Repo


class PhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model=Photo
        fields=['id','oname','uname','size']
        read_only_fields = ['user']
        
class RepoSerializer(serializers.ModelSerializer):
    class Meta:
        model=Repo
        fields='__all__'