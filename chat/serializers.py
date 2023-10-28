from rest_framework import serializers
from .models import Message, Conversation


class ConversationSerializer(serializers.ModelSerializer):
    sender = serializers.StringRelatedField()
    receiver = serializers.StringRelatedField()

    class Meta:
        model = Conversation
        fields = ('id', 'sender', 'receiver', 'room', 'timestamp')
        read_only_fields = ('id', 'timestamp')



class MessageSerializer(serializers.ModelSerializer):

    class Meta:
        model = Message
        fields = ('id', 'sender', 'receiver', 'message', 'is_read', 'timestamp')
        read_only_fields = ('id', 'timestamp')


"""class ConversationSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(many=True)
    messages = MessageSerializer(many=True)"""