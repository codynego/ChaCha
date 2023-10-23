from django.urls import path
from . import views

urlpatterns = [
    path('stories/', views.StoryList.as_view()),


