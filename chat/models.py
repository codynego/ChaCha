from django.db import models
from userauth.models import User

# Create your models here.

class Conversation(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='receivers')
    room = models.UUIDField(auto_created=True, unique=True, editable=False)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.room

    class Meta:
        ordering = ('timestamp',)
        verbose_name_plural = 'Conversations'


class Message(models.Model):
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE, related_name='messages', null="True")
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='receiver')
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)



    def __str__(self):
        return self.message

    class Meta:
        ordering = ('timestamp',)
        verbose_name_plural = 'Messages'
