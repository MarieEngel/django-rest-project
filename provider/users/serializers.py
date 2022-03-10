# Source: https://www.django-rest-framework.org/tutorial/quickstart/

from django.contrib.auth.models import User, Group
from rest_framework import serializers
from .models import Post, Image


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ["url", "username", "email", "groups", "id"]


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ["url", "name"]


class PostSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Post
        fields = ["title", "body", "id"]

class ImageSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Image
        fields = ["caption", "image"]        
