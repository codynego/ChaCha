from rest_framework import serializers
from .models import Story, StoryImage, StoryText, StoryVideo, StoryReaction
from django.contrib.contenttypes.models import ContentType
from django.db.models import Q


class StorySerializer(serializers.ModelSerializer):
    content_type_id = serializers.IntegerField(write_only=True)
    reactions_count = serializers.SerializerMethodField()

    class Meta:
        model = Story
        fields = ('id', 'user', 'object_id', 'content_type_id', 'reactions_count')

    def get_reactions_count(self, obj):
        return obj.story_reactions.count()

    def create(self, validated_data):
        content_type_id = validated_data.pop('content_type_id')
        object_id = validated_data.get('object_id')
        user = validated_data.get('user')

        CONTENT_TYPE_MAP = {
            1: StoryText,
            2: StoryImage,
            3: StoryVideo,
        }

        model_class = CONTENT_TYPE_MAP.get(content_type_id)      

        if model_class is None:
            raise serializers.ValidationError("Invalid content type")
        
        if not model_class.objects.filter(Q(id=object_id)).exists():
            raise serializers.ValidationError("Invalid object id")

        content_object = model_class.objects.get(id=object_id)
        story = Story.objects.create(user=user, content_object=content_object)
        return story


class StoryImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = StoryImage
        fields = '__all__'


class StoryVideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = StoryVideo
        fields = '__all__'


class StoryTextSerializer(serializers.ModelSerializer):
    class Meta:
        model = StoryText
        fields = '__all__'


class StoryReactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = StoryReaction
        fields = '__all__'
