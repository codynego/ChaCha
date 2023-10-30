from django.db import models
from userauth.models import User
import uuid

# Create your models here.

class Conversation(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='receivers')
    room = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.sender.username + " - " + self.receiver.username

    class Meta:
        ordering = ('timestamp',)


    def save(self, *args, **kwargs):
        if not self.room:
            self.room = uuid.uuid4()
        super(Conversation, self).save(*args, **kwargs)


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
