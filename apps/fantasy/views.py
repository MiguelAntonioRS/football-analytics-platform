from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import FantasyTeam, FantasyPlayer, Gameweek, Prediction, Achievement, UserAchievement, Leaderboard, Quiz
from .serializers import (
    FantasyTeamSerializer, FantasyPlayerSerializer, GameweekSerializer,
    PredictionSerializer, AchievementSerializer, LeaderboardSerializer,
    QuizSerializer, QuizQuestionSerializer
)


class FantasyTeamViewSet(viewsets.ModelViewSet):
    serializer_class = FantasyTeamSerializer

    def get_queryset(self):
        if self.action == 'my_team':
            return FantasyTeam.objects.filter(user=self.request.user)
        return FantasyTeam.objects.all()

    @action(detail=False, methods=['get'])
    def my_team(self, request):
        team, created = FantasyTeam.objects.get_or_create(user=request.user, defaults={'name': f"{request.user.username}'s Team"})
        serializer = self.get_serializer(team)
        return Response(serializer.data)

    @action(detail=False, methods=['post'])
    def add_player(self, request):
        team = FantasyTeam.objects.get(user=request.user)
        player_id = request.data.get('player_id')
        position = request.data.get('position', 'FWD')

        from apps.players.models import Player
        real_player = Player.objects.get(id=player_id)
        price = 5000000

        fantasy_player = FantasyPlayer.objects.create(
            real_player=real_player,
            fantasy_team=team,
            position=position,
            price=price
        )
        team.budget -= price
        team.save()

        return Response({'status': 'player added'})


class PredictionViewSet(viewsets.ModelViewSet):
    serializer_class = PredictionSerializer

    def get_queryset(self):
        return Prediction.objects.filter(user=self.request.user)

    @action(detail=False, methods=['get'])
    def available_matches(self, request):
        from apps.matches.models import Match
        from datetime import datetime

        available = Match.objects.filter(
            status='scheduled',
            date__gt=datetime.now()
        ).exclude(
            predictions__user=request.user
        )[:10]

        data = [{
            'id': m.id,
            'match': f"{m.home_team.name} vs {m.away_team.name}",
            'date': m.date
        } for m in available]

        return Response(data)

    @action(detail=False, methods=['post'])
    def submit_prediction(self, request):
        match_id = request.data.get('match_id')
        home_score = request.data.get('home_score')
        away_score = request.data.get('away_score')

        from apps.matches.models import Match
        match = Match.objects.get(id=match_id)

        prediction, created = Prediction.objects.update_or_create(
            user=request.user,
            match=match,
            defaults={'home_score': home_score, 'away_score': away_score}
        )

        return Response({'status': 'prediction saved'})


class AchievementViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Achievement.objects.all()
    serializer_class = AchievementSerializer

    @action(detail=False, methods=['get'])
    def my_achievements(self, request):
        earned = UserAchievement.objects.filter(user=request.user).values_list('achievement_id', flat=True)
        all_achievements = Achievement.objects.all()

        data = []
        for ach in all_achievements:
            data.append({
                **AchievementSerializer(ach).data,
                'is_earned': ach.id in earned
            })

        return Response(data)


class LeaderboardViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Leaderboard.objects.all()
    serializer_class = LeaderboardSerializer

    @action(detail=False, methods=['get'])
    def weekly(self, request):
        entries = Leaderboard.objects.filter(period='weekly').order_by('-points')[:50]
        data = LeaderboardSerializer(entries, many=True).data
        for i, entry in enumerate(data):
            entry['rank'] = i + 1
        return Response(data)

    @action(detail=False, methods=['get'])
    def monthly(self, request):
        entries = Leaderboard.objects.filter(period='monthly').order_by('-points')[:50]
        data = LeaderboardSerializer(entries, many=True).data
        for i, entry in enumerate(data):
            entry['rank'] = i + 1
        return Response(data)

    @action(detail=False, methods=['get'])
    def all_time(self, request):
        entries = Leaderboard.objects.filter(period='all_time').order_by('-points')[:50]
        data = LeaderboardSerializer(entries, many=True).data
        for i, entry in enumerate(data):
            entry['rank'] = i + 1
        return Response(data)


class QuizViewSet(viewsets.ModelViewSet):
    queryset = Quiz.objects.filter(is_active=True)
    serializer_class = QuizSerializer

    @action(detail=True, methods=['post'])
    def submit_answer(self, request, pk=None):
        quiz = self.get_object()
        question_id = request.data.get('question_id')
        answer = request.data.get('answer')

        question = QuizQuestion.objects.get(id=question_id, quiz=quiz)
        is_correct = question.correct_answer == answer

        points = quiz.points_per_question if is_correct else 0

        return Response({
            'is_correct': is_correct,
            'correct_answer': question.correct_answer if not is_correct else None,
            'points': points
        })