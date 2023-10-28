from django.shortcuts import render
from rest_framework import generics
from rest_framework import permissions
from .models import Message
from .serializers import MessageSerializer
from userauth.models import User

# Create your views here.
