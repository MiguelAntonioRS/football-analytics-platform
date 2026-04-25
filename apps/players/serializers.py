from rest_framework import serializers, filters
from .models import Player

class PlayerSerializer(serializers.ModelSerializer):
    team_name = serializers.CharField(source='team.name', read_only=True)
    league_name = serializers.CharField(source='team.league.name', read_only=True)
    age = serializers.IntegerField(read_only=True)
    goals_count = serializers.IntegerField(read_only=True)
    assists_count = serializers.IntegerField(read_only=True)
    yellow_cards = serializers.IntegerField(read_only=True)
    red_cards = serializers.IntegerField(read_only=True)

    class Meta:
        model = Player
        fields = [
            'id', 'name', 'first_name', 'last_name', 'team', 'team_name',
            'league_name', 'position', 'nationality', 'number', 'birth_date',
            'age', 'height', 'weight', 'photo', 'is_active',
            'goals_count', 'assists_count', 'yellow_cards', 'red_cards',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']