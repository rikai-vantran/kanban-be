import ast
from rest_framework import serializers
from .models import Profile
from .models import UserAvatar

class ProfileSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(source='user.id')
    email = serializers.EmailField(source='user.email')
    class Meta:
        model = Profile
        exclude = ['user']
        depth = 1

class ProfileInfoSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(source='user.id', read_only=True)
    email = serializers.EmailField(source='user.email', read_only=True)
    
    class Meta:
        model = Profile
        fields = ['id', 'name', 'profile_pic', 'email']

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        ret['profile_pic'] = UserAvatarSerializer(instance.profile_pic).data
        return ret

class ProfileWorkspaceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['workspace_owner_orders', 'workspace_member_orders']

class UserAvatarSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserAvatar
        fields = '__all__'