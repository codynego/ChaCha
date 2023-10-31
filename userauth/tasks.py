from celery import shared_task
from django.core.mail import send_mail
import time
from .models import User
from .utils import token_generator
from .models import OTP

@shared_task(serializer='json', name="send_mail")
def send_activation_email(user):
    """Send account activation link to the user"""
    activation_code = token_generator()
    otp = OTP.objects.create(otp=activation_code, user=user)
    otp.save()
    message = f"Hello {user.username},\n\nPlease use the following code to activate your account: {activation_code}"

    send_mail(
        subject="Activate your account",
        message=message,
        from_email="codenego@gmail.com",
        recipient_list=[user.email],
        fail_silently=False,
    )