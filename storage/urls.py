from django.urls import path
from . import views

urlpatterns = [
    path('files/',views.getFiles,name='user-info'),
    path('upload/',views.uploadFile,name='uploadFile'),
    path('delete/<int:sid>/',views.deleteFile,name='deleteFile'),
]
