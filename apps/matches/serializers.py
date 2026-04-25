from rest_framework import serializers, filters
from .models import Match, MatchEvent
from apps.teams.serializers import TeamSerializer
from apps.players.serializers import PlayerSerializer

class MatchEventSerializer(serializers.ModelSerializer):
    player_name = serializers.CharField(source='player.name', read_only=True)
    team_name = serializers.CharField(source='team.name', read_only=True)

    class Meta:
        model = MatchEvent
        fields = [
            'id', 'match', 'minute', 'event_type', 'player',
            'player_name', 'team', 'team_name', 'description',
            'is_own_goal', 'created_at'
        ]
        read_only_fields = ['created_at']

class MatchSerializer(serializers.ModelSerializer):
    home_team_name = serializers.CharField(source='home_team.name', read_only=True)
    away_team_name = serializers.CharField(source='away_team.name', read_only=True)
    league_name = serializers.CharField(source='league.name', read_only=True)
    total_goals = serializers.IntegerField(read_only=True)
    events_count = serializers.IntegerField(read_only=True)
    events = MatchEventSerializer(many=True, read_only=True)

    class Meta:
        model = Match
        fields = [
            'id', 'league', 'league_name', 'home_team', 'home_team_name',
            'away_team', 'away_team_name', 'date', 'stadium',
            'home_score', 'away_score', 'total_goals', 'status',
            'round_number', 'attendance', 'referee', 'notes',
            'events_count', 'events', 'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']

class MatchListSerializer(serializers.ModelSerializer):
    home_team_name = serializers.CharField(source='home_team.name', read_only=True)
    away_team_name = serializers.CharField(source='away_team.name', read_only=True)
    league_name = serializers.CharField(source='league.name', read_only=True)
    total_goals = serializers.IntegerField(read_only=True)

    class Meta:
        model = Match
        fields = [
            'id', 'league', 'league_name', 'home_team', 'home_team_name',
            'away_team', 'away_team_name', 'date', 'stadium',
            'home_score', 'away_score', 'total_goals', 'status',
            'round_number'
        ]