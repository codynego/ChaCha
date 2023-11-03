from django.shortcuts import render
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status, viewsets
from rest_framework.views import APIView
from .models import Story, StoryMedia, StoryText, StoryReaction
from .serializers import StorySerializer, StoryMediaSerializer, StoryTextSerializer,\
StoryReactionSerializer
from rest_framework.permissions import IsAuthenticated
from django.db.models import Q
from moviepy.editor import VideoFileClip
import tempfile

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


class StoryMediaAPIView(generics.ListCreateAPIView):
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
    serializer_class = StoryMediaSerializer
    queryset = StoryMedia.objects.all()
    permission_classes = (IsAuthenticated,)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        file = serializer.validated_data['file']
        content_type = file.content_type

        if not content_type.startswith('image/') and not content_type.startswith('video/'):
            return Response({'error': 'Invalid file type'}, status=status.HTTP_400_BAD_REQUEST)
        
        """max_size = 10 * 1024 * 1024
        if file.size > max_size:
            data = {
                "message": "File size is too large.",
                "status": "error",
            }
            return Response({'error': 'File size is too large'}, status=status.HTTP_400_BAD_REQUEST)"""


        if content_type.startswith('video/'):
            # Create a temporary file for processing
            with tempfile.NamedTemporaryFile(suffix='.mp4', delete=False) as temp_file:
                temp_file.write(file.read())
                temp_file_path = temp_file.name

                clip = VideoFileClip(temp_file_path)
                duration = clip.duration
                if duration > 60:
                    # Shorten the video to 1 minute (60 seconds)
                    clip = clip.subclip(0, 60)
                    clip.write_videofile(temp_file_path, threads=4, codec='libx264')

                # Set the authenticated user as the user field
                serializer.validated_data['user'] = request.user

                # Save the processed file back to the serializer
                file.name = temp_file.name
                serializer.validated_data['file'] = file

                self.perform_create(serializer)
                data = {
                    "message": "Story uploaded successfully.",
                    "status": "success",
                    "data": serializer.data
                }
                return Response(data, status=status.HTTP_201_CREATED)

        
        # Set the authenticated user as the user field
        serializer.validated_data['user'] = request.user

        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)






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


        


