from django.db import models
from django.contrib.contenttypes.models import ContentType
from userauth.models import User
from django.contrib.contenttypes.fields import GenericForeignKey

# Create your models here.

class StoryMedia(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='story_medias')
    file = models.FileField(upload_to='stories/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)

class StoryText(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='story_texts')
    text = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)


class Story(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='stories')
    content_type = models.ForeignKey(ContentType, on_delete=models.SET_NULL, null=True)
    object_id = models.PositiveIntegerField(null=True)
    content_object = GenericForeignKey('content_type', 'object_id')
    created_at = models.DateTimeField(auto_now_add=True, null=True)


class StoryReaction(models.Model):
    REACTION_CHOICES = (
        ('like', 'Like'),
        ('love', 'Love'),
        ('haha', 'Haha'),
        ('wow', 'Wow'),
        ('sad', 'Sad'),
        ('angry', 'Angry'),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='story_reactions')
    story = models.ForeignKey(Story, on_delete=models.CASCADE, related_name='story_reactions')
    reaction = models.CharField(max_length=10, choices=REACTION_CHOICES, default='like')





