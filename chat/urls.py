from django.urls import path
from .views import MessageList, ConversationList, SecretKey, ConversationDetail


urlpatterns = [
    path('messages/<str:room_id>/', MessageList.as_view()),
    path('conversations/', ConversationList.as_view()),
    path('secretkey/', SecretKey.as_view()),
    path('conversation/<str:pk>/', ConversationDetail.as_view()),
    #path('conversations/', ConversationListView),
    #path('chat/<str:room_name>/', chat_room, name='chat_room'),
]