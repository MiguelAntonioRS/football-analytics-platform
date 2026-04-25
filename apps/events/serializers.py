from rest_framework import serializers
from .models import Shot, Pass

class ShotSerializer(serializers.ModelSerializer):
    player_name = serializers.CharField(source='player.name', read_only=True)
    team_name = serializers.CharField(source='team.name', read_only=True)

    class Meta:
        model = Shot
        fields = [
            'id', 'match', 'player', 'player_name', 'team', 'team_name',
            'minute', 'x_coordinate', 'y_coordinate', 'distance', 'angle',
            'body_part', 'situation', 'is_goal', 'xg_value', 'created_at'
        ]

class PassSerializer(serializers.ModelSerializer):
    from_player_name = serializers.CharField(source='from_player.name', read_only=True)
    to_player_name = serializers.CharField(source='to_player.name', read_only=True)
    team_name = serializers.CharField(source='team.name', read_only=True)

    class Meta:
        model = Pass
        fields = [
            'id', 'match', 'from_player', 'from_player_name', 'to_player',
            'to_player_name', 'team', 'team_name', 'minute',
            'x_start', 'y_start', 'x_end', 'y_end', 'distance',
            'is_key_pass', 'is_cross', 'is_through_ball', 'successful',
            'assist', 'created_at'
        ]