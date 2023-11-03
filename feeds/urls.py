from django.urls import path
from . import views

urlpatterns = [
    #path('story/', views.StoryAPIView.as_view(), name='story-list'),
    path('story/<int:pk>/', views.StorySingleAPIView.as_view(), name='story'),
    path('story/text/', views.StoryTextAPIView.as_view(), name='story_text'),
    path('story/media/', views.StoryMediaAPIView.as_view(), name='story_media'),
    #path('story/reaction/', views.StoryReactionAPIView.as_view(), name='story_reaction'),
    path('story/reaction/<story_id>/', views.StoryReactionGetAPIView.as_view(), name='story_reaction'),
    path('stories/', views.Stories.as_view(), name='stories'),
    path('feeds/', views.Feeds.as_view(), name='feeds'),

]



