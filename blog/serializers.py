from rest_framework import serializers
from blog.models import *
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework import status
from rest_framework import serializers
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import status
from rest_framework.response import Response
from .models import CustomUser  
from django.db.models import Q

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        username = data.get('username')
        password = data.get('password')

        try:
            user = CustomUser.objects.get(Q(username=username) | Q(email=username))
        except ObjectDoesNotExist:
            raise serializers.ValidationError('Username or email does not exist.')

        if not user.check_password(password):
            raise serializers.ValidationError('Invalid password.')

        if not user.is_active:
            raise serializers.ValidationError('User is not active.')

        data['user'] = user
        return data
    

    def create(self, validated_data):
        user = validated_data['user']
        token, _ = Token.objects.get_or_create(user=user)
        user_data = UserSerializer(user).data  

        return {'token': token.key, 'user': user_data}

    def to_representation(self, instance):
        return instance

    
    
class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = "__all__"
        
        
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"
            

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'city', 'state', 'country', 'email', 'phone', 'first_name', 'last_name', 'gender', 'dob','password']
    def create(self, validated_data):
        password = validated_data.pop('password')
        user = super().create(validated_data)
        user.set_password(password)
        user.save()

        token, _ = Token.objects.get_or_create(user=user)
        user.token = token
        return user

        
class PostSerializer(serializers.ModelSerializer):
    tag = TagSerializer(many=True ,source='tags',read_only=True)
    category = CategorySerializer(source='post_cat',read_only=True)
    auther = UserSerializer(source='author', read_only=True, context={'request': None})
    class Meta:
        model = Post
        fields = "__all__"
   
   
class CommentSerializer(serializers.ModelSerializer):
    post = serializers.SerializerMethodField()
    user = UserSerializer(read_only=True, context={'request': None})  
    parent = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = "__all__"
    def get_post(self, obj):
        post = obj.post
        if post:
            return {'title': post.title}
        return None
    def get_parent(self, obj):
        if obj.parent:
            return CommentSerializer(obj.parent).data
        return None