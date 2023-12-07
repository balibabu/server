from django.urls import path
from . import views

urlpatterns = [
    path('', views.NoteListCreateView.as_view(), name='note-list-create'),
    path('id/<int:pk>/', views.NoteRetrieveUpdateDestroyView.as_view(), name='note-detail'),
]
