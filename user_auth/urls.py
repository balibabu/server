from django.urls import path
from .views import register_api_view, login_api_view,logout_api_view



urlpatterns = [
    path('register/', register_api_view, name='register'),
    path('login/', login_api_view, name='login'),
    path('logout/', logout_api_view, name='logout'),
]
