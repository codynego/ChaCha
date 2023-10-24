from django.shortcuts import render
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from .models import Story, StoryImage, StoryText, StoryVideo, StoryReaction
from .serializers import StorySerializer, StoryImageSerializer, StoryTextSerializer, StoryVideoSerializer, StoryReactionSerializer

# Create your views here.


class StoryAPIView(generics.ListAPIView):
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


class StorySingleAPIView(generics.RetrieveDestroyAPIView):
    queryset = Story.objects.all()
    serializer_class = StorySerializer



class StoryReactionAPIView(generics.ListCreateAPIView):
    queryset = StoryReaction.objects.all()
    serializer_class = StoryReactionSerializer

class StoryReactionGetAPIView(APIView):
    def get(self, request, story_id):
        story = Story.objects.get(id=story_id)
        reactions = StoryReaction.objects.filter(story=story)
        serializer = StoryReactionSerializer(reactions, many=True)
        response_data = {
            "message": "Story reactions fetched successfully!",
            "statusCode": status.HTTP_200_OK,
            "data": serializer.data
        }
        return Response(response_data, status=status.HTTP_200_OK)
    
    def post(self, request, story_id):
        story = Story.objects.get(id=story_id)
        serializer = StoryReactionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(story=story)
            response_data = {
                "message": "Story reaction created successfully!",
                "statusCode": status.HTTP_201_CREATED,
                "data": serializer.data
            }
            return Response(response_data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
