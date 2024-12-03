from rest_framework import serializers
from .models import Profile

class ProfileSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Profile
        fields = '__all__'

    def update(self, instance, validated_data):
        if 'workspace_member_orders' in validated_data:
            print('workspace_member_orders')
        return super().update(instance, validated_data)