from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import generics, viewsets
from .serializers import *


# Create your views here.


class BlogPostView(viewsets.ModelViewSet):
    serializer_class = BlogPostSerializer
    queryset = BlogPost.objects.all()
