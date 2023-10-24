from django.shortcuts import render
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from .models import Story, StoryImage, StoryText, StoryVideo, StoryReaction
from .serializers import StorySerializer, StoryImageSerializer, StoryTextSerializer, StoryVideoSerializer, StoryReactionSerializer
from rest_framework.permissions import IsAuthenticated

# Create your views here.


class StoryAPIView(generics.ListAPIView):
    queryset = Story.objects.all()
    serializer_class = StorySerializer
    permission_classes = (IsAuthenticated,)

class StoryTextAPIView(generics.ListCreateAPIView):
    queryset = StoryText.objects.all()
    serializer_class = StoryTextSerializer
    #permission_classes = (IsAuthenticated,)

class StoryImageAPIView(generics.ListCreateAPIView):
    queryset = StoryImage.objects.all()
    serializer_class = StoryImageSerializer
    permission_classes = (IsAuthenticated,)

class StoryVideoAPIView(generics.ListCreateAPIView):
    queryset = StoryVideo.objects.all()
    serializer_class = StoryVideoSerializer
    permission_classes = (IsAuthenticated,)


class StorySingleAPIView(generics.RetrieveDestroyAPIView):
    queryset = Story.objects.all()
    serializer_class = StorySerializer
    permission_classes = (IsAuthenticated,)



class StoryReactionGetAPIView(generics.ListCreateAPIView):
    queryset = StoryReaction.objects.all()
    serializer_class = StoryReactionSerializer
    permission_classes = (IsAuthenticated,)



        


