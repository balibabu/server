from django.urls import path
from . import views

urlpatterns = [
    path('filesAndFolders/',views.getFilesAndFolders,name='user-info'),
    path('files/',views.getFiles,name='user-info'),
    path('upload/',views.uploadFile,name='uploadFile'),
    path('delete/<int:sid>/',views.deleteFile,name='deleteFile'),
    path('download/<int:file_id>/',views.downloadFile,name='downloadFile'),
    path('gits/',views.getGitInfo,name='gits-info'),
    path('folder/',views.FolderListCreateView.as_view(),name='folder-create-list'),

]
