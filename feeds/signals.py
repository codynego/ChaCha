from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import Story, StoryImage, StoryVideo, StoryText

@receiver(post_save, sender=StoryImage)
@receiver(post_save, sender=StoryVideo)
@receiver(post_save, sender=StoryText)
def create_story_on_content_creation(sender, instance, created, **kwargs):
    if created:
        Story.objects.create(user=instance.user, content_object=instance)


@receiver(post_delete, sender=Story)
def delete_story_content_on_story_deletion(sender, instance, **kwargs):
    content_object = instance.content_object
    if isinstance(content_object, StoryImage) or isinstance(content_object, StoryVideo) or isinstance(content_object, StoryText):
        if not content_object._state.adding:
            content_object.delete()
    else:
        print("Content object not found!")