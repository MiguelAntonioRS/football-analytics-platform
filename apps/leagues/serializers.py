from rest_framework import serializers, filters
from .models import League

class LeagueSerializer(serializers.ModelSerializer):
    teams_count = serializers.IntegerField(read_only=True)
    matches_count = serializers.IntegerField(read_only=True)
    total_goals = serializers.IntegerField(read_only=True)

    class Meta:
        model = League
        fields = [
            'id', 'name', 'country', 'season', 'logo', 'description',
            'teams_count', 'matches_count', 'total_goals',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']