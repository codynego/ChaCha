from django.shortcuts import render
from rest_framework import generics
from rest_framework import permissions
from .models import Message
from .serializers import MessageSerializer, ConversationSerializer
from userauth.models import User
from django.db.models import Q
from rest_framework.response import Response
from userauth.serializers import UserSerializer

# Create your views here.


class MessageList(generics.ListAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = MessageSerializer

    def get_queryset(self, *args, **kwargs):
        user = self.request.user
        receiver_id = self.kwargs['receiver']
        receiver = User.objects.get(id=receiver_id)
        messages = Message.objects.filter(Q(sender=user, receiver=receiver)).order_by('timestamp')
    
    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = MessageSerializer(queryset, many=True)


class ConversationList(generics.ListAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = MessageSerializer

    def get_queryset(self):
        user = self.request.user
        receiver = self.kwargs['receiver']
        return Message.objects.filter(Q(sender=user) | Q(receiver=user)).order_by('timestamp')

    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        all_conversations = []
        for conversations in queryset:
            if conversations.sender or conversations.receiver not in all_conversations:
                all_conversations.append(conversations.sender)
                all_conversations.append(conversations.receiver)
        
        serializer = UserSerializer(all_conversations, many=True)
        return Response(serializer.data)