from rest_framework import serializers
from .models import *


class BlogPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = BlogPost
        exclude = []

# class BlogListSerializer(serializers.ModelSerializer)
