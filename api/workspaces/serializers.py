from rest_framework import serializers
from api.models import Workspaces, Profile
from api.profiles.serializers import ProfileInfoSerializer

class WorkspaceInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Workspaces
        fields = ['id', 'name', 'icon_unified']

class WorkspaceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Workspaces
        fields = '__all__'
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['members'] = ProfileInfoSerializer(instance.members.all(), many=True).data
        return representation

class WorkspaceMembersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Workspaces.members.through
        fields = '__all__'

class AddMembersSerializer(serializers.Serializer):
    id = serializers.ListField(child=serializers.IntegerField())

    def validate_id(self, value):
        for id in value:
            # check duplicate id
            if value.count(id) > 1:
                raise serializers.ValidationError('Duplicate id')
            # check exits user
            if not Profile.objects.filter(user_id=id).exists():
                raise serializers.ValidationError('User does not exist')
        return value
