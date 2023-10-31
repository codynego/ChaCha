# import send email function
from django.core.mail import send_mail
from django.contrib.auth import get_user_model
from django.utils import timezone
import string
import random


def token_generator(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


def checkOTPExpiration(otp):
    """Check if the otp is expired or not"""
    if otp:
        now = timezone.now()
        time_difference = now - otp.created_at
        if time_difference.seconds > 300:
            return False
        else:
            return True
    else:
        return False