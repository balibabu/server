from django.urls import path
from . import views,viewsFolder

urlpatterns = [
    path('filesAndFolders/',viewsFolder.getFilesAndFolders,name='user-info'),
    path('gits/',views.getGitInfo,name='gits-info'),

    path('files/',views.getFiles,name='user-info'),
    path('upload/',views.uploadFile,name='uploadFile'),
    path('delete/<int:sid>/',views.deleteFile,name='deleteFile'),
    path('download/<int:file_id>/',views.downloadFile,name='downloadFile'),
    path('file/<int:pk>/',views.UpdateFileView.as_view(),name='file-update'),

    path('folder/',viewsFolder.FolderListCreateView.as_view(),name='folder-create-list'),
    path('folder/<int:pk>/',viewsFolder.FolderUpdateDeleteView.as_view(),name='folder-update-delete'),
]
