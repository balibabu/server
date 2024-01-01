from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .models import Note
from .serializers import NoteSerializer, NoteListSerializer

class NoteListCreateView(generics.ListCreateAPIView):
    serializer_class = NoteSerializer
    permission_classes = [IsAuthenticated]

    # def get_serializer_class(self):              # uncomment this line for getting only titles and comment the above serializer
    #     if self.request.method == 'GET':
    #         return NoteListSerializer
    #     return NoteSerializer

    def get_queryset(self):
        return Note.objects.filter(user=self.request.user).order_by('-created_time')

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class NoteRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = NoteSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Note.objects.filter(user=self.request.user)
