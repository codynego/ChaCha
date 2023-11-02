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
    Create and list story text.

    This endpoint allows authenticated users to create and list story text.

    ---
    HTTP Methods:
      - POST: Create a new story text.
      - GET: List existing story text.

    Request (POST):
      - Requires authentication.
      - JSON body: {"text": "This is a sample story text."}

    Response (GET):
      - List of story texts.

    Authentication:
      - Authentication is required for both POST and GET requests.

    Example:
    ```
    POST /api/story/text/
    Request:
    {
        "text": "This is a sample story text."
    }
    Response:
    {
        "id": 1,
        "text": "This is a sample story text.",
        ...
    }

    """
    queryset = StoryText.objects.all()
    serializer_class = StoryTextSerializer
    permission_classes = (IsAuthenticated,)

class StoryImageAPIView(generics.ListCreateAPIView):
    """
    This endpoint allows authenticated users to create and list story image.

    HTTP Methods:
        - POST: Create a new story image.
        - GET: List existing story image.

    Request (POST):
        - Requires authentication.
        - JSON body: {"image": "image.jpg"}

    Response (GET):
        - List of story images.

    Authentication:
        - Authentication is required for both POST and GET requests.
    """
    queryset = StoryImage.objects.all()
    serializer_class = StoryImageSerializer
    permission_classes = (IsAuthenticated,)

class StoryVideoAPIView(generics.ListCreateAPIView):
    """
    This endpoint allows authenticated users to create and list story video.

    HTTP Methods:
        - POST: Create a new story video.
        - GET: List existing story video.

    Request (POST):
        - Requires authentication.
        - JSON body: {"video": "video.mp4"}

    Response (GET):
        - List of story videos.

    Authentication:
        - Authentication is required for both POST and GET requests.

    """
    queryset = StoryVideo.objects.all()
    serializer_class = StoryVideoSerializer
    permission_classes = (IsAuthenticated,)


class StorySingleAPIView(generics.RetrieveDestroyAPIView):
    """
    This endpoint allows authenticated users to retrieve and delete a story.

    HTTP Methods:
        - GET: Retrieve a story.
        - DELETE: Delete a story.
    
    Request (GET):
        - Requires authentication.
    
    Response (GET):
        - Story details.

    Request (DELETE):
        - Requires authentication.

    Response (DELETE):
        - Success message.

    Authentication:
        - Authentication is required for both GET and DELETE requests.
    """
    queryset = Story.objects.all()
    serializer_class = StorySerializer
    permission_classes = (IsAuthenticated,)



class StoryReactionGetAPIView(generics.ListCreateAPIView):
    """
    This endpoint allows authenticated users to create and list story reactions.

    HTTP Methods:
        - POST: Create a new story reaction.
        - GET: List existing story reactions.

    Request (POST):
        - Requires authentication.
        - JSON body: {"reaction": "like"}

    Response (GET):
        - List of story reactions.

    Authentication:
        - Authentication is required for both POST and GET requests.
    """

    queryset = StoryReaction.objects.all()
    serializer_class = StoryReactionSerializer
    permission_classes = (IsAuthenticated,)


class Stories(generics.ListAPIView):
    """
    This endpoint allows authenticated users to list stories.

    HTTP Methods:
        - GET: List existing stories.

    Response (GET):
        - List of stories.

    Authentication:
        - Authentication is required for GET requests.
    """
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
    """
    This endpoint allows authenticated users to list feeds.

    HTTP Methods:
        - GET: List existing feeds.

    Response (GET):
        - List of feeds.

    Authentication:
        - Authentication is required for GET requests.
    """
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


        


