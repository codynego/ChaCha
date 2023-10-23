from rest_framework import serializers
from .models import Story, StoryImage, StoryText, StoryVideo
from django.contrib.contenttypes.models import ContentType


class StorySerializer(serializers.ModelSerializer):
    content_object_id = serializers.IntegerField(write_only=True)  # Add this field to accept content object ID

    class Meta:
        model = Story
        fields = ('id', 'user', 'content_type', 'object_id', 'content_object_id')

    # Rest of the serializer code...

    def create(self, validated_data):
        content_object_id = validated_data.pop('content_object_id')
        content_type = validated_data.get('content_type')
        user = validated_data.get('user')

        CONTENT_TYPE_MAP = {
            1: StoryText,
            2: StoryImage,
            3: StoryVideo,
        }

        model_class = CONTENT_TYPE_MAP.get(content_type)
        if model_class is None:
            raise serializers.ValidationError("Invalid content type")
        
        content_object = model_class.objects.get(id=content_object_id)
        story = Story.objects.create(user=user, content_object=content_object)
        return story


class StoryImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Story
        fields = '__all__'


class StoryVideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Story
        fields = '__all__'


class StoryTextSerializer(serializers.ModelSerializer):
    class Meta:
        model = Story
        fields = '__all__'
