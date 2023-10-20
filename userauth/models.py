from django.db import models
from django.contrib.auth.models import AbstractBaseUSer, PermissionMixin
from django.utils import timezone
from .managers import CustomUserManager

class User(AbstractBaseUSer, PermissionMixin):
    email = models.EmailField(blank=True, default='', unique=True)
    first_name = models.CharField(max_length=100, null=True, blank=True)
    last_name = models.CharField(max_length=100, null=True, blank=True)
    username = models.CharField(max_length=100, null=True, blank=True, unique=True)
    phone_number = models.PositiveIntegerField(null=True)
    birth_date = models.DateField(null=True, blank=True)
    bio = models.TextField(null=True, blank=True)
    interest = models.CharField(max_length=100, null=True, blank=True)
    verified = models.BooleanField(default=False)
    review = models.CharField(max_length=100, null=True, blank=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', null=True, blank=True)


    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    date_joined = models.DateTimeField(default=timezone.now)
    last_seen = models.DateTimeField(default='')

    objects = CustomUserManager()


    USERNAME_FIELD = 'username'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = []


    class Meta:
        verbose_name = 'user'
        verbose_name_plural = 'users'


    def __str__(self):
        return self.username