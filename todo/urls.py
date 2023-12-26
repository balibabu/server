from django.urls import path
from . import views

urlpatterns = [
    path('',views.TodoListCreateView.as_view(),name='todo-list-create'),
    path('completed/',views.TodoCompletedList.as_view(),name='todo-completed-list'),
    path('id/<int:pk>/',views.TodoRetrieveUpdateDestroyView.as_view(),name='todo-update'),
]
