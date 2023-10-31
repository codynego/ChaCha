from django.shortcuts import render
from rest_framework.views import APIView, status
from .serializers import RegistrationSerializer, UserSerializer, ReviewSerializer, FollowSerializer, InterestSerializer, VerifyEmailSerializer
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import generics
from .models import User, Review, Interest
from rest_framework import authentication
from rest_framework import permissions
from .tasks import send_activation_email
from .utils import checkOTPExpiration
from .models import OTP
#import get_or_404
from django.shortcuts import get_object_or_404
from .utils import token_generator

# Create your views here.

class RegistrationAPIView(generics.CreateAPIView):
    serializer_class = RegistrationSerializer

    
    def post(self, request):
        serializer = RegistrationSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            response_data = {
                "message": "User registered successfully!",
                "statusCode": status.HTTP_201_CREATED,
                "data": serializer.data
            }
            send_activation_email.delay(serializer.instance)
            return Response(response_data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        

class VerifyEmailAPIView(generics.CreateAPIView):
    serializer_class = VerifyEmailSerializer

    def post(self, request, *args, **kwargs):
        data = request.data
        serializer =  self.serializer_class(data=data)

        if serializer.is_valid():
            otp = serializer.validated_data.get('otp')
            email = serializer.validated_data.get('email')
            if User.objects.filter(email=email).exists():
                user = User.objects.get(email=email)
            else:
                response_data = {
                "message": "User does not exist! Please register.",
                "statusCode": status.HTTP_400_BAD_REQUEST,
                }
                return Response(response_data, status=status.HTTP_400_BAD_REQUEST)
            if OTP.objects.filter(otp=otp).exists():
                get_otp = OTP.objects.get(otp=otp)
            else:
                response_data = {
                "message": "Invalid OTP! Please try again.",
                "statusCode": status.HTTP_400_BAD_REQUEST,
                }
                return Response(response_data, status=status.HTTP_400_BAD_REQUEST)
            if checkOTPExpiration(get_otp):
                user.is_active = True
                user.is_verified = True
                user.save()
                get_otp.delete()
                response_data = {
                "message": "User verified successfully!",
                "statusCode": status.HTTP_200_OK,
                }
                return Response(response_data, status=status.HTTP_200_OK)
            else:
                get_otp.delete()
                response_data = {
                "message": "OTP expired!",
                "statusCode": status.HTTP_400_BAD_REQUEST,
                }
                return Response(response_data, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        


class ResendVerifyEmailAPIView(generics.CreateAPIView):
    serializer_class = VerifyEmailSerializer

    def post(self, request, *args, **kwargs):
        data = request.data
        serializer =  self.serializer_class(data=data)

        if serializer.is_valid():
            email = serializer.validated_data.get('email')
            user = get_object_or_404(User, email=email)
            if user.is_verified:
                response_data = {
                "message": "User already verified!",
                "statusCode": status.HTTP_400_BAD_REQUEST,
                }
                return Response(response_data, status=status.HTTP_400_BAD_REQUEST)
            else:
                send_activation_email.delay(user)
                response_data = {
                    "message": "OTP sent successfully!",
                    "statusCode": status.HTTP_200_OK,
                    }
                return Response(response_data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserAPIView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user
    
    def get(self, request, *args, **kwargs):
        serializer = UserSerializer(self.get_object())
        response_data = {
            "message": "User details fetched successfully!",
            "statusCode": status.HTTP_200_OK,
            "data": serializer.data
        }
        return Response(response_data, status=status.HTTP_200_OK)
    
    def put(self, request, *args, **kwargs):
        serializer = UserSerializer(self.get_object(), data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            response_data = {
                "message": "User details updated successfully!",
                "statusCode": status.HTTP_200_OK,
                "data": serializer.data
            }
            return Response(response_data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    def delete(self, request, *args, **kwargs):
        self.get_object().delete()
        response_data = {
            "message": "User deleted successfully!",
            "statusCode": status.HTTP_200_OK,
        }
        return Response(response_data, status=status.HTTP_200_OK)
    

class FollowUserAPIView(APIView):
    def post(self, request, user_id):
        user = request.user
        user_to_follow = User.objects.get(id=user_id)
        user.following.add(user_to_follow)
        response_data = {
            "message": "User followed successfully!",
            "statusCode": status.HTTP_200_OK,
        }
        return Response(response_data, status=status.HTTP_200_OK)
    

class UnfollowUserAPIView(APIView):
    def post(self, request, user_id):
        user = request.user
        user_to_unfollow = User.objects.get(id=user_id)
        user.following.remove(user_to_unfollow)
        response_data = {
            "message": "User unfollowed successfully!",
            "statusCode": status.HTTP_200_OK,
        }
        return Response(response_data, status=status.HTTP_200_OK)
    

class FollowersAPIView(APIView):
    def get(self, request):
        user = request.user
        serializer = FollowSerializer(user.followers, many=True)
        response_data = {
            "message": "Followers fetched successfully!",
            "statusCode": status.HTTP_200_OK,
            "data": serializer.data
        }
        return Response(response_data, status=status.HTTP_200_OK)
    

class FollowingAPIView(APIView):
    def get(self, request):
        user = request.user
        serializer = FollowSerializer(user.following, many=True)
        response_data = {
            "message": "Following fetched successfully!",
            "statusCode": status.HTTP_200_OK,
            "data": serializer.data
        }
        return Response(response_data, status=status.HTTP_200_OK)
    


class ReviewAPIView(APIView):
    #authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        user = request.user
        review_count, avg_review = user.get_review_count()
        reviews = Review.objects.filter(reviewed_user=user)
        serializer = ReviewSerializer(reviews, many=True)
        response_data = {
            "message": "Review fetched successfully!",
            "statusCode": status.HTTP_200_OK,
            "review_count": review_count,
            "avg_review": avg_review,
            "reviews": serializer.data
        }
        return Response(response_data, status=status.HTTP_200_OK)

    def post(self, request):
        user = request.user
        data = request.data

        reviewed_user_id = data.get('reviewed_user')

        try:
            reviewed_usr = User.objects.get(pk=reviewed_user_id)
        except User.DoesNotExist:
            return Response({"message": "Invalid 'reviewed_user' ID"}, status=status.HTTP_400_BAD_REQUEST)

        serializer = ReviewSerializer(data=data, context={'user': user, 'reviewed_user': reviewed_usr})

        if serializer.is_valid():
            serializer.save()
            response_data = {
                "message": "Review posted successfully!",
                "statusCode": status.HTTP_201_CREATED,
            "data": serializer.validated_data
            }
            return Response(response_data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        

class InterestAPIView(generics.ListCreateAPIView):
    queryset = Interest.objects.all()
    serializer_class = InterestSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        user = self.request.user
        return Interest.objects.filter(user=user)
    
    def post(self, request):
        user = request.user
        data = request.data
        serializer = InterestSerializer(data=data, context={'user': user})

        if serializer.is_valid():
            serializer.save()
            response_data = {
                "message": "Interest added successfully!",
                "statusCode": status.HTTP_201_CREATED,
            "data": serializer.validated_data
            }
            return Response(response_data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        






