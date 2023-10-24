#a function that automatically deletes a story from the database after 24 hours using django-cron
from django_cron import CronJobBase, Schedule
from feeds.models import Story, StoryImage, StoryVideo, StoryText
from datetime import timedelta
from django.utils import timezone

class DeleteStory(CronJobBase):
    RUN_EVERY_MINS = 1  # every 1 minute

    schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
    code = 'feeds.delete_story'

    def do(self):
        now = timezone.now()
        stories = Story.objects.filter(created_at__lt=now - timedelta(hours=24))
        storyText = StoryText.objects.filter(created_at__lt=now - timedelta(hours=24))
        storyVideo = StoryVideo.objects.filter(created_at__lt=now - timedelta(hours=24))
        storyImage = StoryImage.objects.filter(created_at__lt=now - timedelta(hours=24))
        stories.delete()
        storyText.delete()
        storyVideo.delete()
        storyImage.delete()