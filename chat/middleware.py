from rest_framework_simplejwt.tokens import UntypedToken
from channels.db import database_sync_to_async
from django.contrib.auth.models import AnonymousUser
from django.conf import settings
import jwt
from django.conf import settings
from django.contrib.auth import get_user_model
from rest_framework.exceptions import AuthenticationFailed

User = get_user_model()

@database_sync_to_async
def get_user(access_token):
    try:
        # Decode the access token using the secret key
        decoded_payload = jwt.decode(access_token, settings.SECRET_KEY, algorithms=['HS256'])
        
        # Extract the user ID from the decoded payload
        user_id = decoded_payload.get('user_id')
        
        # Retrieve the user based on the extracted user ID
        user = User.objects.get(id=user_id)
        print(user.username)
        
        return user
    except jwt.ExpiredSignatureError:
        # Handle expired token
        raise AuthenticationFailed('Access token has expired.')
    except jwt.InvalidTokenError:
        # Handle invalid token
        raise AuthenticationFailed('Invalid access token.')
    except User.DoesNotExist:
        # Handle user not found
        raise AuthenticationFailed('User not found.')







class TokenAuthMiddleware:
    def __init__(self, inner):
        # Store the ASGI application we were passed
        self.inner = inner
        
    async def __call__(self, scope, receive, send):
        try:
            # Extract token from the Authorization header
            headers = dict(scope["headers"])
            auth_header = headers.get(b'authorization').decode()
            token_type, token = auth_header.split(' ')
            if token_type.lower() == 'bearer':
                scope['user'] = await get_user(token)
        except Exception as e:
            # Handle the exception (e.g., log it)
            scope['user'] = None

        return await self.inner(scope, receive, send)
