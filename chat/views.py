from django.shortcuts import render
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework import permissions
from .models import Message, Conversation
from .serializers import MessageSerializer, ConversationSerializer
from userauth.models import User
from django.db.models import Q
from rest_framework.response import Response
from userauth.serializers import UserSerializer
from .utils import generate_keys

# Create your views here.


class ConversationList(generics.ListCreateAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = ConversationSerializer

    def get_queryset(self):
        user = self.request.user
        return Conversation.objects.filter(Q(sender=user) | Q(receiver=user)).order_by('timestamp')

    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = ConversationSerializer(queryset, many=True)
        data = {
            "message": "Conversations retrieved successfully.",
            "status": "success",
            "data": serializer.data
        }
        return Response(data)
    
    def post(self, request, *args, **kwargs):
        receiver_id = self.request.data['receiver']
        receiver = User.objects.get(id=receiver_id)
        if Conversation.objects.filter(Q(sender=request.user, receiver=receiver) | Q(sender=receiver, receiver=request.user)).exists():
            conversation = Conversation.objects.get(Q(sender=request.user, receiver=receiver) | Q(sender=receiver, receiver=request.user))
            serializer = ConversationSerializer(conversation)
            return Response(serializer.data)
        serializer = ConversationSerializer(data=request.data, context={'request': request, 'receiver': receiver})
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)
    

class ConversationDetail(generics.DestroyAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = ConversationSerializer
    queryset = Conversation.objects.all()

    
    def delete(self, request, *args, **kwargs):
        if Conversation.objects.filter(room=self.kwargs['pk']).exists():
            conversation = Conversation.objects.get(room=self.kwargs['pk'])
            conversation.delete()
            data = {
                "message": "Conversation deleted successfully.",
                "status": "success"
            }
            return Response(data)
        else:
            data = {
                "message": "Conversation does not exist.",
                "status": "error"
            }
            return Response(data)


class MessageList(generics.ListAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = MessageSerializer

    def get_queryset(self, *args, **kwargs):
        user = self.request.user
        room = self.kwargs['room_id']
        conversation = Conversation.objects.get(room=self.kwargs['room_id'])
        #receiver = User.objects.get(id=receiver_id)
        messages = Message.objects.filter(conversation__room=room).order_by('timestamp')
        return messages
    
    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = MessageSerializer(queryset, many=True)
        data = {
            "message": "Messages retrieved successfully.",
            "status": "success",
            "data": serializer.data
        }
        return Response(data)
    

class SecretKey(APIView):
    #permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        private_key, public_key = generate_keys()
        secret_key = {
            'private_key': private_key.decode('utf-8'),
            'public_key': public_key.decode('utf-8')
        }
        return Response(secret_key)




"""class ConversationList(generics.ListAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = MessageSerializer

    def get_queryset(self):
        user = self.request.user
        return Message.objects.filter(Q(sender=user) | Q(receiver=user)).order_by('timestamp')

    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        all_conversations = []
        for conversations in queryset:
            if conversations.sender or conversations.receiver not in all_conversations:
                if conversations.sender == request.user:
                    all_conversations.append(conversations.receiver)
                else:
                    all_conversations.append(conversations.sender)
        all_conversations = set(all_conversations)
        
        serializer = UserSerializer(all_conversations, many=True)
        return Response(serializer.data)"""

"""def ConversationListView(request):
    user = request.user
    queryset = Message.objects.filter(Q(sender=user) | Q(receiver=user)).order_by('timestamp')
    all_conversations = []
    for conversations in queryset:
        if conversations.sender or conversations.receiver not in all_conversations:
            if conversations.sender == request.user:
                all_conversations.append(conversations.receiver)
            else:
                all_conversations.append(conversations.sender)
    all_conversations = set(all_conversations)
    context = {
        'all_conversations': all_conversations
    }
    return render(request, 'chat/conversation_list.html', context)"""


"""def chat_room(request, room_name):
    return render(request, 'chat/chat.html', {
        'room_name': room_name
    })"""