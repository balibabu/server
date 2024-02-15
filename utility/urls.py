from django.urls import path
from . import views

urlpatterns = [
    path('clip/sync/', views.sync_clip, name='testnig'),
    path('file/share/', views.file_share, name='testnig'),
    # path('db-backup/', views.db_backup, name='backupDB'),
]
