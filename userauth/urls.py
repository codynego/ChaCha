from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from django.urls import path
from . views import( RegistrationAPIView, UserAPIView, 
                    FollowUserAPIView, UnfollowUserAPIView, ReviewAPIView, 
                    FollowersAPIView, FollowingAPIView, InterestAPIView, VerifyEmailAPIView,
                    ResendVerifyEmailAPIView
                    )

urlpatterns = [
    # authentication endpoints
    path('auth/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('auth/user/register', RegistrationAPIView.as_view(), name='register'),
    path('auth/user/verify-email', VerifyEmailAPIView.as_view(), name='verify_email'),
    path('auth/user/resend-verify-email', ResendVerifyEmailAPIView.as_view(), name='resend_verify_email'),


    # user endpoints
    path('user/me/', UserAPIView.as_view(), name='user'),
    path('user/follow/', FollowUserAPIView.as_view(), name='follow_user'),
    path('user/unfollow/', UnfollowUserAPIView.as_view(), name='unfollow_user'),
    path('user/review/', ReviewAPIView.as_view(), name='review_user'),
    path('user/followers/', FollowersAPIView.as_view(), name='followers'),
    path('user/following/', FollowingAPIView.as_view(), name='following'),
    path('user/interest/', InterestAPIView.as_view(), name='interest'),

]