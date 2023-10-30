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

        # Join room group

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
        message = text_data_json['message']
        await self.save_message(message)
        await self.channel_layer.group_send(
        self.room_group_name,
            {
                'type': 'chat_message',
                'message': message
            }
        )

    async def chat_message(self, event):
        message = event['message']
        await self.send(text_data=json.dumps({
            'message': message
        }))

    @database_sync_to_async
    def save_message(self, message):
        room_name = self.scope['url_route']['kwargs']['room_name']
        conversation = Conversation.objects.get(room=room_name)

        new_message = Message.objects.create(
            sender=self.user,
            receiver=conversation.receiver,
            conversation=conversation,
            message=message
        )

        new_message.save()

