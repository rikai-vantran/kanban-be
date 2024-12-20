from rest_framework import serializers
from api.kanban_board.models import Columns
from api.kanban_board.models import Cards
from api.kanban_board.models import Tasks

class ColumnSerializer(serializers.ModelSerializer):
    class Meta:
        model = Columns
        fields = '__all__'

class CardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cards
        fields = '__all__'

class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tasks
        fields = ['id', 'content', 'status', 'card']