from rest_framework import generics
from .models import Todo
from .serializers import TodoSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied


class TodoListCreateView(generics.ListCreateAPIView):
    serializer_class = TodoSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Todo.objects.filter(user=self.request.user).order_by('-created_time')

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class TodoRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Todo.objects.all()
    serializer_class = TodoSerializer

    def check_permission(self, todo_instance, action):
        if todo_instance.user != self.request.user:
            raise PermissionDenied(f"You do not have permission to {action} this Todo.")

    def update(self, request, *args, **kwargs):
        todo_instance = self.get_object()
        self.check_permission(todo_instance, 'update')
        return super().update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        todo_instance = self.get_object()
        self.check_permission(todo_instance, 'delete')
        return super().destroy(request, *args, **kwargs)