from rest_framework import serializers
from .models import FantasyTeam, FantasyPlayer, Gameweek, Prediction, Achievement, UserAchievement, Leaderboard, Quiz, QuizQuestion


class FantasyPlayerSerializer(serializers.ModelSerializer):
    player_name = serializers.CharField(source='real_player.name', read_only=True)
    team_name = serializers.CharField(source='real_player.team.name', read_only=True)

    class Meta:
        model = FantasyPlayer
        fields = ['id', 'real_player', 'player_name', 'team_name', 'position', 'price', 'is_captain', 'is_vice_captain', 'is_bench']


class FantasyTeamSerializer(serializers.ModelSerializer):
    players = FantasyPlayerSerializer(many=True, read_only=True)

    class Meta:
        model = FantasyTeam
        fields = ['id', 'name', 'budget', 'points', 'players', 'created_at']


class GameweekSerializer(serializers.ModelSerializer):
    class Meta:
        model = Gameweek
        fields = ['id', 'number', 'start_date', 'end_date', 'is_active', 'deadline']


class PredictionSerializer(serializers.ModelSerializer):
    match_info = serializers.SerializerMethodField()

    class Meta:
        model = Prediction
        fields = ['id', 'match', 'match_info', 'home_score', 'away_score', 'points', 'is_correct', 'created_at']

    def get_match_info(self, obj):
        return f"{obj.match.home_team.name} vs {obj.match.away_team.name}"


class AchievementSerializer(serializers.ModelSerializer):
    is_earned = serializers.SerializerMethodField()

    class Meta:
        model = Achievement
        fields = ['id', 'name', 'description', 'icon', 'category', 'requirement', 'points_reward', 'is_earned']

    def get_is_earned(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return UserAchievement.objects.filter(user=request.user, achievement=obj).exists()
        return False


class LeaderboardSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)

    class Meta:
        model = Leaderboard
        fields = ['id', 'user', 'username', 'points', 'rank', 'period']


class QuizQuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuizQuestion
        fields = ['id', 'question', 'option_a', 'option_b', 'option_c', 'option_d']


class QuizSerializer(serializers.ModelSerializer):
    questions = QuizQuestionSerializer(many=True, read_only=True)

    class Meta:
        model = Quiz
        fields = ['id', 'title', 'description', 'question_count', 'points_per_question', 'questions']