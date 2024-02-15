from django.urls import path
from . import views



urlpatterns = [
    path('', views.get_user_info, name='get_user_info'),
    path('register/', views.register_api_view, name='register'),
    path('login/', views.login_api_view, name='login'),
    path('logout/', views.logout_api_view, name='logout'),
]
