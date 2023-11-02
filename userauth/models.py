from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.utils import timezone
from .managers import CustomUserManager
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db.models import Avg

class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(blank=True, default='', unique=True)
    first_name = models.CharField(max_length=100, null=True, blank=True)
    last_name = models.CharField(max_length=100, null=True, blank=True)
    username = models.CharField(max_length=100, null=True, blank=True, unique=True)
    phone_number = models.CharField(max_length=15, null=True, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    bio = models.TextField(null=True, blank=True)
    interest = models.ManyToManyField('Interest', blank=True, related_name='users')
    rating = models.FloatField(default=0, null=True, blank=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', null=True, blank=True)
    public_key = models.CharField(max_length=100, null=True, blank=True)
    followers = models.ManyToManyField('self', blank=True, symmetrical=False, related_name='following')
    
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    date_joined = models.DateTimeField(default=timezone.now)
    open_to_chat = models.BooleanField(default=False)
    last_seen = models.DateTimeField(default=timezone.now)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    class Meta:
        verbose_name = 'user'
        verbose_name_plural = 'users'

    def __str__(self):
        return self.username
    
    def get_review_count(self):
        review = Review.objects.filter(reviewed_user=self)
        review_count = review.count()
        avg_review = review.aggregate(Avg('rating'))['rating__avg']
        self.rating = avg_review
        self.save() 
        return review_count, avg_review
    

class OTP(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='otp')
    otp = models.CharField(max_length=6, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.otp


class Review(models.Model):
    RATINGS = (
        (1, '1'),
        (2, '2'),
        (3, '3'),
        (4, '4'),
        (5, '5')
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews')
    reviewed_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviewed_users')
    content = models.TextField(null=True, blank=True)
    rating = models.PositiveSmallIntegerField(choices=RATINGS, default=1)
    created_at = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return f"Review by {self.user.username} for {self.reviewed_user.username}"
    

class Interest(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='interests', null=True, blank=True)
    name = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return self.name