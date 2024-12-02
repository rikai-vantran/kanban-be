from rest_framework import serializers
from django.contrib.auth.models import User
from api.models import Profile

class RegisterSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    username = serializers.CharField(max_length=200, required=True)
    password = serializers.CharField(max_length=200, required=True, write_only=True)
    
    def validate_email(self,value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError('Email already exists.')
        return value
    def validate_username(self,value):
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError('Username already exists.')
        return value

    def create(self, validated_data):
        user = User.objects.create_user(validated_data['username'], validated_data['email'], validated_data['password'])
        Profile.objects.create(user=user, name=validated_data['username'])
        return {'username': user.username, 'email': user.email}