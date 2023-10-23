from django.shortcuts import render
from rest_framework import generics
from .models import Story, StoryImage, StoryText, StoryVideo, StoryReaction
from .serializers import StorySerializer, StoryImageSerializer, StoryTextSerializer, StoryVideoSerializer, StoryReactionSerializer

# Create your views here.


class StoryAPIView(generics.ListCreateAPIView):
    queryset = Story.objects.all()
    serializer_class = StorySerializer

class StoryTextAPIView(generics.ListCreateAPIView):
    queryset = StoryText.objects.all()
    serializer_class = StoryTextSerializer

class StoryImageAPIView(generics.ListCreateAPIView):
    queryset = StoryImage.objects.all()
    serializer_class = StoryImageSerializer

class StoryVideoAPIView(generics.ListCreateAPIView):
    queryset = StoryVideo.objects.all()
    serializer_class = StoryVideoSerializer


class StoryReactionAPIView(generics.ListCreateAPIView):
    queryset = StoryReaction.objects.all()
    serializer_class = StoryReactionSerializer

class StoryReactionGetAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = StoryReaction.objects.all()
    serializer_class = StoryReactionSerializer

    def get_object(self):
        story_id = self.kwargs.get('story_id')
        return StoryReaction.objects.get(story=story_id)
