from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Count, Q
from apps.analytics.services import StatisticsService
from apps.analytics.serializers import (
    TeamStatsSerializer, PlayerStatsSerializer, LeagueStatsSerializer,
    MatchEventsSummarySerializer, AnalyticsDataSerializer
)
from apps.analytics.models import AnalyticsData
from apps.players.models import Player
from apps.teams.models import Team
from apps.leagues.models import League
from apps.matches.models import Match

class TeamStatisticsView(APIView):
    def get(self, request, team_id):
        try:
            stats = StatisticsService.get_team_statistics(team_id)
            serializer = TeamStatsSerializer(stats)
            return Response(serializer.data)
        except Team.DoesNotExist:
            return Response({'error': 'Equipo no encontrado'}, status=status.HTTP_404_NOT_FOUND)

class PlayerStatisticsView(APIView):
    def get(self, request, player_id):
        try:
            stats = StatisticsService.get_player_statistics(player_id)
            serializer = PlayerStatsSerializer(stats)
            return Response(serializer.data)
        except Player.DoesNotExist:
            return Response({'error': 'Jugador no encontrado'}, status=status.HTTP_404_NOT_FOUND)

class TopScorersView(APIView):
    def get(self, request):
        limit = int(request.query_params.get('limit', 10))
        league_id = request.query_params.get('league')
        season = request.query_params.get('season')

        players = StatisticsService.get_top_scorers(limit, league_id, season)
        data = []
        for player in players:
            stats = StatisticsService.get_player_statistics(player.id)
            data.append(stats)

        serializer = PlayerStatsSerializer(data, many=True)
        return Response(serializer.data)

class TopAssistsView(APIView):
    def get(self, request):
        limit = int(request.query_params.get('limit', 10))
        league_id = request.query_params.get('league')
        season = request.query_params.get('season')

        players = StatisticsService.get_top_assists(limit, league_id, season)
        data = []
        for player in players:
            stats = StatisticsService.get_player_statistics(player.id)
            data.append(stats)

        serializer = PlayerStatsSerializer(data, many=True)
        return Response(serializer.data)

class LeagueStatisticsView(APIView):
    def get(self, request, league_id):
        try:
            stats = StatisticsService.get_league_statistics(league_id)
            serializer = LeagueStatsSerializer(stats)
            return Response(serializer.data)
        except League.DoesNotExist:
            return Response({'error': 'Liga no encontrada'}, status=status.HTTP_404_NOT_FOUND)

class MatchEventsSummaryView(APIView):
    def get(self, request, match_id):
        try:
            stats = StatisticsService.get_match_events_summary(match_id)
            serializer = MatchEventsSummarySerializer(stats)
            return Response(serializer.data)
        except Match.DoesNotExist:
            return Response({'error': 'Partido no encontrado'}, status=status.HTTP_404_NOT_FOUND)

class SeasonStatisticsView(APIView):
    def get(self, request, season):
        stats = StatisticsService.get_season_statistics(season)
        return Response(stats)

class DashboardDataView(APIView):
    def get(self, request):
        total_leagues = League.objects.count()
        total_teams = Team.objects.count()
        total_players = Player.objects.count()
        total_matches = Match.objects.filter(status='finished').count()

        total_goals = sum(
            m.home_score + m.away_score
            for m in Match.objects.filter(status='finished')
        )

        top_scorers = []
        for player in StatisticsService.get_top_scorers(5):
            stats = StatisticsService.get_player_statistics(player.id)
            top_scorers.append(stats)

        top_assists = []
        for player in StatisticsService.get_top_assists(5):
            stats = StatisticsService.get_player_statistics(player.id)
            top_assists.append(stats)

        recent_matches = Match.objects.filter(status='finished').order_by('-date')[:5]

        data = {
            'summary': {
                'total_leagues': total_leagues,
                'total_teams': total_teams,
                'total_players': total_players,
                'total_matches': total_matches,
                'total_goals': total_goals,
                'avg_goals_per_match': total_goals / total_matches if total_matches > 0 else 0,
            },
            'top_scorers': PlayerStatsSerializer(top_scorers, many=True).data,
            'top_assists': PlayerStatsSerializer(top_assists, many=True).data,
            'recent_matches': [
                {
                    'id': m.id,
                    'home_team': m.home_team.name,
                    'away_team': m.away_team.name,
                    'home_score': m.home_score,
                    'away_score': m.away_score,
                    'date': m.date,
                }
                for m in recent_matches
            ]
        }

        return Response(data)