from rest_framework import serializers, filters
from .models import Team

class TeamSerializer(serializers.ModelSerializer):
    league_name = serializers.CharField(source='league.name', read_only=True)
    players_count = serializers.IntegerField(read_only=True)
    total_matches = serializers.IntegerField(read_only=True)

    class Meta:
        model = Team
        fields = [
            'id', 'name', 'league', 'league_name', 'stadium', 'coach',
            'logo', 'founded_year', 'website', 'players_count',
            'total_matches', 'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']