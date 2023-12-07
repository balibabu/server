from django.urls import path
from . import views

urlpatterns = [
    path('',views.TodoListCreateView.as_view(),name='todo-list-create'),
    path('id/<int:pk>/',views.TodoRetrieveUpdateDestroyView.as_view(),name='todo-update'),
]
