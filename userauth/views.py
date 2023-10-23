from django.shortcuts import render
from rest_framework.views import APIView, status
from .serializers import RegistrationSerializer, UserSerializer
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import generics


# Create your views here.

class RegistrationAPIView(APIView):
    def post(self, request):
        serializer = RegistrationSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            response_data = {
                "message": "User registered successfully!",
                "statusCode": status.HTTP_201_CREATED,
                "data": serializer.validated_data
            }
            return Response(response_data, status=status.HTTP_201_CREATED)
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
    

