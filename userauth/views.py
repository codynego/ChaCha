from django.shortcuts import render
from rest_framework.views import APIView, status
from .serializers import RegistrationSerializer
from rest_framework.response import Response


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