from django.http import Http404
from rest_framework import status
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from django.contrib.auth.models import User, Group
from rest_framework import viewsets
from rest_framework import permissions
from rest_framework.views import APIView
from .serializers import UserSerializer, GroupSerializer, PostSerializer, ImageSerializer
from .models import Post, Image


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


# class PostList(APIView):
#     """
#     List all posts, or create a new post.
#     """

#     def get(self, request, format=None):
#         posts = Post.objects.all()
#         serializer = PostSerializer(posts, many=True)
#         return Response(serializer.data)

#     def post(self, request, format=None):
#         serializer = PostSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# class PostDetail(APIView):
#     """
#     Retrieve, update or delete a snippet instance.
#     """

#     def get_object(self, id):
#         try:
#             return Post.objects.get(pk=id)
#         except Post.DoesNotExist:
#             raise Http404

#     def get(self, request, id, format=None):
#         post = self.get_object(id)
#         serializer = PostSerializer(post)
#         return Response(serializer.data)

#     def put(self, request, id, format=None):
#         post = self.get_object(id)
#         serializer = PostSerializer(post, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#     def delete(self, request, id, format=None):
#         post = self.get_object(id)
#         post.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)


class PostViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.


    """
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]

class ImageView(APIView):
    parser_classes = (MultiPartParser, FormParser)

    def get(self, request):
        image_objects = Image.objects.all()
        serializer = ImageSerializer(image_objects, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        file_serializer = ImageSerializer(data=request.data)
        if file_serializer.is_valid():
            file_serializer.save()
            return Response(file_serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(file_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

