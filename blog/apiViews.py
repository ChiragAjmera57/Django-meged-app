from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from rest_framework import viewsets, filters
from rest_framework.pagination import PageNumberPagination

from blog.serializers import *
from blog.models import *

class LoginViewSet(viewsets.ModelViewSet):
    queryset = []  
    http_method_names = ['post']
    serializer_class = LoginSerializer
 
  
class UserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    http_method_names = ['get']
    serializer_class = UserSerializer
    
class UserSignViewSet(viewsets.ModelViewSet):
    queryset = []
    http_method_names = ['post']
    serializer_class = UserSerializer
    

class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    filter_backends = [filters.SearchFilter,DjangoFilterBackend,filters.OrderingFilter]
    search_fields = ['title', 'text','author__username']   
    ordering_fields = ['created_date'] 
    lookup_field = 'post_slug'  
    pagination_class = PageNumberPagination
    filterset_fields = ["tags","post_cat","author"]
    http_method_names = ['post','get','patch']
       

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["title"]
    http_method_names = ['post','get','patch']

class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    filter_backends = [filters.SearchFilter,DjangoFilterBackend]
    search_fields = ['text', 'name','body']   
    http_method_names = ['post','get','patch']
    
class TagViewSet(viewsets.ModelViewSet):   
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    filter_backends = [DjangoFilterBackend,filters.SearchFilter]
    search_fields = ['name']   
    filterset_fields = ["name"]
    http_method_names = ['post','get','patch']

    
    
