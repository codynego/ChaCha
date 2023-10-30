from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from userauth.models import User
from rest_framework.authtoken.models import Token


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        token = Token.objects.create(user=instance)
        token.save()