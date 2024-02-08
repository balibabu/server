from django.urls import path, include
from . import views
from .extra import ws_views

urlpatterns = [
    path('users/', views.UserListView.as_view(), name='user-list'),
    path('send-message/<int:userid>/', views.send_message, name='send-message'),
    path('conversations/', views.user_conversations, name='latest_messages'),
    path('conversations/<int:userid>/', views.full_conversation, name='get_all_msg_with_user_x'),


    ###### extra features ### for imitating weshocket
    path('new-msg/<int:msgid>/<int:senderid>/',ws_views.get_new_messages,name="get_new_messages"),
    path('cend/',ws_views.send_msg_get_latest_msg,name='send-msg-and-get-msg')
]