from rest_framework import serializers
from .models import Story, StoryImage, StoryText, StoryVideo, StoryReaction
from django.contrib.contenttypes.models import ContentType
from django.db.models import Q


from rest_framework import serializers
from .models import Story, StoryText, StoryImage, StoryVideo
from django.db.models import Q

class StorySerializer(serializers.ModelSerializer):
    content = serializers.SerializerMethodField()
    reactions_count = serializers.SerializerMethodField()

    class Meta:
        model = Story
        fields = ('id', 'user', 'object_id', 'content', 'reactions_count')

    def get_reactions_count(self, obj):
        return obj.story_reactions.count()

    def get_content(self, obj):
        content_object = obj.content_object
        print(content_object)
        if isinstance(content_object, StoryText):
            return content_object.text
        elif isinstance(content_object, StoryImage):
            return content_object.image.url
        elif isinstance(content_object, StoryVideo):
            return content_object.video.url
        else:
            return None

    
    def to_representation(self, instance):
        representation = super(StorySerializer, self).to_representation(instance)
        representation['content'] = self.get_content(instance)
        return representation



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
    story_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = StoryReaction
        fields = '__all__'

    def create(self, validated_data):
        story_id = validated_data.pop('story_id')
        story = Story.objects.get(id=story_id)
        reaction = StoryReaction.objects.create(story=story, **validated_data)
        return reaction