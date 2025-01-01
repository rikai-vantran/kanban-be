from rest_framework import serializers
from api.models import Workspaces, Profile
from api.profiles.serializers import ProfileInfoSerializer
from api.models import WorkspaceLabels

class WorkspaceMemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = Workspaces.members.through
        exclude = ['workspace', 'member', 'id']
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        # add extra data
        profile = Profile.objects.get(user_id=instance.member_id)
        representation['profile'] = ProfileInfoSerializer(profile).data
        return representation

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
        # add many to many field extra data
        representation['members'] = WorkspaceMemberSerializer(instance.members.through.objects.filter(workspace=instance), many=True).data
        representation['labels'] = WorkspaceLabelSerializer(instance.labels_set.all(), many=True).data
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

class WorkspaceLabelSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkspaceLabels
        fields = '__all__'