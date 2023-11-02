import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from .models import Message
from userauth.models import User
from .models import Conversation

class ChatConsumer(AsyncWebsocketConsumer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.room_name = None
        self.room_group_name = None
        self.user = None

    async def connect(self):
        self.user = self.scope['user']
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name

        if self.user.is_authenticated:
            await self.channel_layer.group_add(
                self.room_group_name,
                self.channel_name
            )
            await self.accept()
        else:
            await self.close()

    async def disconnect(self, close_code):
        room_name = self.scope['url_route']['kwargs']['room_name']
        print(f"WebSocket disconnected from room '{room_name}'.")
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        
        if 'message' in text_data_json:
            # Message handling
            message = text_data_json['message']
            await self.save_message(message)
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'chat_message',
                    'message': message
                }
            )

        elif 'shared_key' in text_data_json:
            # Shared key handling
            shared_key = text_data_json['shared_key']
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'send_shared_key',
                    'shared_key': shared_key
                }
            )

        elif 'symmetric_key' in text_data_json:
            symmetric_key = text_data_json['symmetric_key']
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'send_symmetric_key',
                    'symmetric_key': symmetric_key
                }
            )

    async def chat_message(self, event):
        message = event['message']
        conversation = Conversation.objects.get(room=self.room_name)
        await self.send(text_data=json.dumps({
            'type': 'message',
            'sender': conversation.sender.username,
            'receiver': conversation.receiver.username,
            'message': message
        }))

    async def send_shared_key(self, event):
        shared_key = event['shared_key']
        await self.send(text_data=json.dumps({
            'type': 'shared_key',
            'shared_key': shared_key
        }))

    async def send_symmetric_key(self, event):
        symmetric_key = event['symmetric_key']
        await self.send(text_data=json.dumps({
            'type': 'symmetric_key',
            'symmetric_key': symmetric_key
        }))

    @database_sync_to_async
    def save_message(self, message):
        room_name = self.scope['url_route']['kwargs']['room_name']
        conversation = Conversation.objects.get(room=room_name)

        new_message = Message.objects.create(
            conversation=conversation,
            message=message,
            is_read=False
        )

        new_message.save()
