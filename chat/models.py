from django.db import models
from userauth.models import User

# Create your models here.


class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='receivers')
    room = models.CharField(max_length=100)
    message = models.TextField(max_length=1000)
    is_read = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.message

    class Meta:
        ordering = ('timestamp',)
        verbose_name_plural = 'Messages'
