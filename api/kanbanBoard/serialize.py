from rest_framework import serializers
from api.kanbanBoard.models import Columns
from api.kanbanBoard.models import Cards
from api.profiles.serializers import ProfileInfoSerializer
from api.workspaces.models import Workspaces

class ColumnSerializer(serializers.ModelSerializer):
    class Meta:
        model = Columns
        fields = '__all__'

class CardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cards
        fields = '__all__'

    def validate(self, attrs):
        workspace = Workspaces.objects.get(id=self.context['workspace_id'])
        if attrs.get('assigns') != None:
            for member in attrs['assigns']:
                if member not in workspace.members.all():
                    raise serializers.ValidationError('Member not in workspace')            
        return attrs
    
    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['assigns'] = ProfileInfoSerializer(instance.assigns.all(), many=True).data
        return response