from rest_framework import serializers
from .models import Message, Conversation


class ConversationSerializer(serializers.ModelSerializer):
    sender = serializers.StringRelatedField()
    receiver = serializers.StringRelatedField()

    class Meta:
        model = Conversation
        fields = ('id', 'sender', 'receiver', 'room', 'timestamp')
        read_only_fields = ('id', 'timestamp')


    def create(self, validated_data):
        sender = self.context['request'].user
        receiver = self.context['receiver']
        conversation = Conversation.objects.create(sender=sender, receiver=receiver)
        return conversation



class MessageSerializer(serializers.ModelSerializer):
    conversation = ConversationSerializer()

    class Meta:
        model = Message
        fields = ('id', 'conversation', 'message', 'is_read', 'timestamp')
        read_only_fields = ('id', 'timestamp')

    
    def get_conversation(self, obj):
        conversation_data = self.conversation.data
        conversation_data.pop('timestamp', None)
        return conversation_data


"""class ConversationSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(many=True)
    messages = MessageSerializer(many=True)"""