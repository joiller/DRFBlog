from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import generics, viewsets, filters, status
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


@api_view(['GET'])
def get_parents(request, category_slug):
    category = Category.objects.filter(slug=category_slug)
    if category:
        print(category[0].get_parents(json=True))
        return Response(category[0].get_parents(json=True))
    return Response({'error': 'no such category'}, status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
def get_children(request, category_slug):
    category = Category.objects.filter(slug=category_slug)
    if category:
        return Response(category[0].get_children(json=True))
    return Response({'error': 'no such category'})
