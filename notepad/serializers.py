from rest_framework import serializers
from .models import Note

class NoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Note
        fields = ('id', 'user', 'title', 'description', 'created_time','color','modified_time')
        read_only_fields = ['user']

class NoteListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Note
        fields = ('id', 'user', 'title', 'created_time','color','modified_time')


class NoteSyncSerializer(serializers.ModelSerializer):
    class Meta:
        model=Note
        fields=('id','modified_time')