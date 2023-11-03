from django.contrib import admin
from .models import Story, StoryMedia, StoryText
# Register your models here.

admin.site.register(Story)
admin.site.register(StoryMedia)
admin.site.register(StoryText)


