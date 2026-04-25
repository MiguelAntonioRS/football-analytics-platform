from rest_framework import serializers
from apps.analytics.models import AnalyticsData
from apps.analytics.services import StatisticsService
from apps.teams.serializers import TeamSerializer
from apps.players.serializers import PlayerSerializer

class TeamStatsSerializer(serializers.Serializer):
    team = TeamSerializer()
    total_matches = serializers.IntegerField()
    wins = serializers.IntegerField()
    draws = serializers.IntegerField()
    losses = serializers.IntegerField()
    goals_for = serializers.IntegerField()
    goals_against = serializers.IntegerField()
    win_rate = serializers.FloatField()
    goals_per_match = serializers.FloatField()

class PlayerStatsSerializer(serializers.Serializer):
    player = PlayerSerializer()
    total_matches = serializers.IntegerField()
    goals = serializers.IntegerField()
    assists = serializers.IntegerField()
    shots = serializers.IntegerField()
    passes = serializers.IntegerField()
    fouls = serializers.IntegerField()
    yellow_cards = serializers.IntegerField()
    red_cards = serializers.IntegerField()
    tackles = serializers.IntegerField()
    goals_per_match = serializers.FloatField()
    assists_per_match = serializers.FloatField()

class LeagueStatsSerializer(serializers.Serializer):
    league = serializers.CharField()
    total_matches = serializers.IntegerField()
    total_goals = serializers.IntegerField()
    avg_goals_per_match = serializers.FloatField()
    teams = TeamStatsSerializer(many=True)

class MatchEventsSummarySerializer(serializers.Serializer):
    match = serializers.IntegerField()
    goals = serializers.IntegerField()
    assists = serializers.IntegerField()
    shots = serializers.IntegerField()
    fouls = serializers.IntegerField()
    yellow_cards = serializers.IntegerField()
    red_cards = serializers.IntegerField()
    tackles = serializers.IntegerField()
    by_team = serializers.DictField()

class AnalyticsDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = AnalyticsData
        fields = [
            'id', 'match', 'home_possession', 'away_possession',
            'home_shots', 'away_shots', 'home_shots_on_target', 'away_shots_on_target',
            'home_passes', 'away_passes', 'home_pass_accuracy', 'away_pass_accuracy',
            'home_fouls', 'away_fouls', 'home_corners', 'away_corners',
            'home_yellow_cards', 'away_yellow_cards', 'home_red_cards', 'away_red_cards',
            'home_offsides', 'away_offsides', 'created_at', 'updated_at'
        ]