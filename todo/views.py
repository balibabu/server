from rest_framework import generics
from .models import Todo
from .serializers import TodoSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied


class TodoListCreateView(generics.ListCreateAPIView):
    queryset = Todo.objects.order_by('-created_time')
    serializer_class = TodoSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class TodoUpdateView(generics.UpdateAPIView):
    queryset=Todo.objects.all()
    serializer_class=TodoSerializer

    def update(self, request, *args, **kwargs):
        todo_instance = self.get_object()

        if todo_instance.user != request.user:
            raise PermissionDenied("You do not have permission to update this Todo.")

        return super().update(request, *args, **kwargs)