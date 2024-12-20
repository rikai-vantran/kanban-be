from rest_framework import serializers
from api.kanbanBoard.models import Columns
from api.kanbanBoard.models import Cards
from api.profiles.serializers import ProfileSerializer

class ColumnSerializer(serializers.ModelSerializer):
    class Meta:
        model = Columns
        fields = '__all__'

class CardSerializer(serializers.ModelSerializer):
    assigns = ProfileSerializer(many=True, read_only=True)
    class Meta:
        model = Cards
        fields = '__all__'