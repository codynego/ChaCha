from django.contrib.auth.models import AnonymousUser
from channels.db import database_sync_to_async
from rest_framework.authtoken.models import Token
from channels.middleware import BaseMiddleware
# import simple jwt token
from rest_framework_simplejwt.tokens import AccessToken



@database_sync_to_async
def get_user(token_key):
    try:
        token = AccessToken(token_key)
        return token.user
    except Token.DoesNotExist:
        return AnonymousUser()