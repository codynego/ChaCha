from django.urls import path
from .views import MessageList, ConversationList


urlpatterns = [
    path('messages/<int:receiver>/', MessageList.as_view()),
    path('conversations/', ConversationList.as_view()),
    #path('conversations/', ConversationListView),
    #path('chat/<str:room_name>/', chat_room, name='chat_room'),
]