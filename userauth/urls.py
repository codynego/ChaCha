from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from django.urls import path
from .views import RegistrationAPIView, UserAPIView, FollowUserAPIView, UnfollowUserAPIView, ReviewAPIView, FollowersAPIView, FollowingAPIView

urlpatterns = [
    path('auth/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('auth/user/register', RegistrationAPIView.as_view(), name='register'),
    path('user/me/', UserAPIView.as_view(), name='user'),
    path('user/follow/', FollowUserAPIView.as_view(), name='follow_user'),
    path('user/unfollow/', UnfollowUserAPIView.as_view(), name='unfollow_user'),
    path('user/review/', ReviewAPIView.as_view(), name='review_user'),
    path('user/<int:user_id>/followers/', FollowersAPIView.as_view(), name='followers'),
    path('user/<int:user_id>/following/', FollowingAPIView.as_view(), name='following'),
    path('user/<int:user_id>/reviews/', ReviewAPIView.as_view(), name='reviews'),
]