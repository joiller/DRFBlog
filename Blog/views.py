from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import generics, viewsets, filters
from .serializers import *


# Create your views here.


class BlogPostView(viewsets.ModelViewSet):
    serializer_class = BlogPostSerializer
    queryset = BlogPost.objects.all()


class BlogListView(generics.ListAPIView):
    serializer_class = BlogPostSerializer
    queryset = BlogPost.objects.all()
    filter_backends = [filters.SearchFilter]
    search_fields = ['author__username', 'title', 'id', 'body']
