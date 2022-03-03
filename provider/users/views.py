# Source: https://www.django-rest-framework.org/tutorial/quickstart/
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt

from django.contrib.auth.models import User, Group
from rest_framework import viewsets
from rest_framework import permissions
from rest_framework.parsers import JSONParser
from .serializers import UserSerializer, GroupSerializer, PostSerializer
from .models import Post


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """

    queryset = User.objects.all().order_by("-date_joined")
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """

    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [permissions.IsAuthenticated]

class PostViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows posts to be viewed or edited.
    """    
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]

# @csrf_exempt
# def post_list(request):
#     """
#     List all posts, or create a new post.
#     """
#     if request.method == 'GET':
#         posts = Post.objects.all()
#         serializer = PostSerializer(posts, many=True)
#         return JsonResponse(serializer.data, safe=False)

#     elif request.method == 'POST':
#         data = JSONParser().parse(request)
#         serializer = PostSerializer(data=data)
#         if serializer.is_valid():
#             serializer.save()
#             return JsonResponse(serializer.data, status=201)
#         return JsonResponse(serializer.errors, status=400)  

# @csrf_exempt
# def post_detail(request, pk):
#     """
#     Retrieve, update or delete a post.
#     """
#     try:
#         post = Post.objects.get(pk=pk)
#     except Post.DoesNotExist:
#         return HttpResponse(status=404)

#     if request.method == 'GET':
#         serializer = PostSerializer(post)
#         return JsonResponse(serializer.data)

#     elif request.method == 'PUT':
#         data = JSONParser().parse(request)
#         serializer = PostSerializer(post, data=data)
#         if serializer.is_valid():
#             serializer.save()
#             return JsonResponse(serializer.data)
#         return JsonResponse(serializer.errors, status=400)

#     elif request.method == 'DELETE':
#         post.delete()
#         return HttpResponse(status=204)
