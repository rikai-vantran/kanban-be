from rest_framework import serializers
from api.models import WorkspaceMembers

class GetAllWorkSpaceSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(source='workspace.id')
    name = serializers.CharField(source='workspace.name')
    icon_unified = serializers.CharField(source='workspace.icon_unified')
    column_orders = serializers.JSONField(source='workspace.column_orders')
    class Meta:
        model = WorkspaceMembers
        fields = ['id', 'name', 'icon_unified', 'column_orders']


class WorkspaceSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=128)
    icon_unified = serializers.CharField(max_length=128)
    column_orders = serializers.JSONField()

class GetWorkspaceSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField(max_length=128)
    icon_unified = serializers.CharField(max_length=128)
    column_orders = serializers.JSONField()
    create_at = serializers.DateTimeField()
    members = GetAllWorkSpaceSerializer(many=True)
    logs = serializers.JSONField()
    class Meta:
        model = WorkspaceMembers
        fields = ['id', 'name', 'icon_unified', 'column_orders', 'create_at', 'members', 'logs']
