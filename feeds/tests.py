from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import Story
from .serializers import StorySerializer

class StoryAPITestCase(APITestCase):
    def setUp(self):
        self.url = reverse('story-list')  # Assuming you have a URL name for the StoryAPIView

        # Create some example Story objects for testing
        self.story1 = Story.objects.create(user=self.user1, content_type=self.content_type1, object_id=1)
        self.story2 = Story.objects.create(user=self.user2, content_type=self.content_type2, object_id=2)

    def test_list_stories(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Deserialize the response data and check if it matches the created stories
        serializer = StorySerializer(Story.objects.all(), many=True)
        self.assertEqual(response.data, serializer.data)

    def test_list_stories_empty(self):
        # Create an empty queryset by deleting the previously created stories
        Story.objects.all().delete()
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)

    # Add more test cases as needed
