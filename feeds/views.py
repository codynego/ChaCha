from django.shortcuts import render
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from .models import Story, StoryImage, StoryText, StoryVideo, StoryReaction
from .serializers import StorySerializer, StoryImageSerializer, StoryTextSerializer,\
StoryVideoSerializer, StoryReactionSerializer, StoriesSerializer
from rest_framework.permissions import IsAuthenticated
from django.db.models import Q

# Create your views here.

class StoryTextAPIView(generics.ListCreateAPIView):
    """
    This endpoint allows for creation and listing of story text.

    Authentication required.
    body: {
        "text": "This is a sample story text."
    }
    """

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


class Stories(generics.ListAPIView):
    queryset = Story.objects.all()
    serializer_class = StorySerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        user = self.request.user
        queryset = Story.objects.filter(Q(user=user) | Q(user__in=user.following.all()))
        return queryset
    
    def get(self, request, *args, **kwargs):
        user = request.user
        queryset = self.get_queryset()
        serializer = StorySerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    

class Feeds(generics.ListAPIView):
    queryset = Story.objects.all()
    serializer_class = StorySerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        user = self.request.user
        queryset = Story.filter(user__interest__in=user.interests.all())
        return queryset
    
    def get(self, request, *args, **kwargs):
        user = request.user
        queryset = self.get_queryset()
        serializer = StorySerializer(queryset, many=True)

        data = {
            "message": "Stories retrieved successfully.",
            "status": "success",
            "data": serializer.data
        }
        return Response(data, status=status.HTTP_200_OK)


        


