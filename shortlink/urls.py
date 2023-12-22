from django.urls import path
from . import views

urlpatterns = [
    path('',views.LinkCreateView.as_view(),name='LinkCreateView'),
    path('id/<int:pk>/',views.LinkRetrieve.as_view(),name='LinkRetrieve'),
]
