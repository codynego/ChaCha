from django.contrib import admin
from .models import Story, StoryImage, StoryText, StoryVideo

# Register your models here.

admin.site.register(Story)
admin.site.register(StoryImage)
admin.site.register(StoryText)
admin.site.register(StoryVideo)

