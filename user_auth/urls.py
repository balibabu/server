from django.urls import path
from .views import get_user_info,register_api_view, login_api_view,logout_api_view,test



urlpatterns = [
    path('', get_user_info, name='get_user_info'),
    path('register/', register_api_view, name='register'),
    path('login/', login_api_view, name='login'),
    path('logout/', logout_api_view, name='logout'),
    path('test/', test, name='logout'),
]
