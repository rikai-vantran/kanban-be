from api.models import Request, Workspaces
from rest_framework import serializers
from api.profiles.serializers import ProfileInfoSerializer
from api.workspaces.serializers import WorkspaceInfoSerializer

class RequestSerializer(serializers.ModelSerializer):
    user_sender = serializers.PrimaryKeyRelatedField(read_only=True)
    status = serializers.CharField(default='pending')
    class Meta:
        model = Request
        fields = '__all__'

    def validate(self, data):
        user_receiver = data['user_receiver']
        workspace = data['workspace']
        if Workspaces.objects.filter(id=workspace.id).exists() == False:
            raise serializers.ValidationError("The workspace does not exist.")
        if Request.objects.filter(user_receiver=user_receiver, workspace=workspace, status='pending').exists():
            raise serializers.ValidationError("User already has a request for this workspace.")
        return data
    
    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['user_sender'] = ProfileInfoSerializer(instance.user_sender).data
        response['user_receiver'] = ProfileInfoSerializer(instance.user_receiver).data
        response['workspace'] = WorkspaceInfoSerializer(instance.workspace).data
        return response

class AcceptRejectRequestSerializer(serializers.Serializer):
    status = serializers.CharField()
    
    def validate(self, data):
        status = data.get('status')
        if status not in ['accepted', 'rejected']:
            raise serializers.ValidationError("The status must be either 'accepted' or 'rejected'.")   
        return data