from django.urls import path
from . import views

urlpatterns = [
    path('',views.getPhotos,name='get-photos'),
    path('upload/',views.upload,name='upload-photos'),
    path('download/<int:id>/',views.download,name='upload-photos'),
    path('thumbnail/<str:uname>/',views.getAThumbnail,name='get-thumbnails'),
    path('thumbnails/ping/',views.getThumbnailsReady,name='getThumbnailsReady'),
]
