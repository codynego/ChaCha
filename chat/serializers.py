from rest_framework import serializers
from .models import Message


class MessageSerializer(serializers.ModelSerializer):

    class Meta:
        model = Message
        fields = ('id', 'sender', 'receiver', 'message', 'is_read', 'timestamp')
        read_only_fields = ('id', 'timestamp')


class ConversationSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(many=True)
    messages = MessageSerializer(many=True)