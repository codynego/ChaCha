from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Story, StoryImage, StoryVideo, StoryText

@receiver(post_save, sender=StoryImage)
@receiver(post_save, sender=StoryVideo)
@receiver(post_save, sender=StoryText)
def create_story_on_content_creation(sender, instance, created, **kwargs):
    if created:
        Story.objects.create(user=instance.user, content_object=instance)



@receiver(post_save, sender=StoryImage)
@receiver(post_save, sender=StoryVideo)
@receiver(post_save, sender=StoryText)
def delete_story_on_content_creation(sender, instance, created, **kwargs):
    if created:
        Story.objects.create(user=instance.user, content_object=instance)
