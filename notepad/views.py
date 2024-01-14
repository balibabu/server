from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .models import Note
from .serializers import NoteSerializer, NoteSyncSerializer

class NoteListCreateView(generics.ListCreateAPIView):
    serializer_class = NoteSerializer
    permission_classes = [IsAuthenticated]
    def get_queryset(self):
        return Note.objects.filter(user=self.request.user).order_by('-created_time')
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class NoteRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = NoteSerializer
    permission_classes = [IsAuthenticated]
    def get_queryset(self):
        return Note.objects.filter(user=self.request.user)


class NoteSyncListView(generics.ListAPIView):
    serializer_class=NoteSyncSerializer
    permission_classes=[IsAuthenticated]
    def get_queryset(self):
        return Note.objects.filter(user=self.request.user)

class NoteListByIdView(generics.ListAPIView):
    serializer_class = NoteSerializer
    permission_classes = [IsAuthenticated]
    def get_queryset(self):
        note_ids_header = self.request.headers.get('ids', '')
        note_ids = [int(id) for id in note_ids_header.split(',') if id.isdigit()]
        return Note.objects.filter(user=self.request.user, id__in=note_ids).order_by('-created_time')