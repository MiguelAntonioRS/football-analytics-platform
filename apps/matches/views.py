from rest_framework import viewsets, filters
from .models import Match, MatchEvent
from .serializers import MatchSerializer, MatchListSerializer, MatchEventSerializer

class MatchViewSet(viewsets.ModelViewSet):
    queryset = Match.objects.all()
    serializer_class = MatchSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['home_team__name', 'away_team__name', 'stadium']
    ordering_fields = ['date', 'home_score', 'away_score', 'created_at']
    ordering = ['-date']

    def get_serializer_class(self):
        if self.action == 'list':
            return MatchListSerializer
        return MatchSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        league_id = self.request.query_params.get('league')
        team_id = self.request.query_params.get('team')
        status = self.request.query_params.get('status')
        from_date = self.request.query_params.get('from_date')
        to_date = self.request.query_params.get('to_date')

        if league_id:
            queryset = queryset.filter(league_id=league_id)
        if team_id:
            queryset = queryset.filter(home_team_id=team_id) | queryset.filter(away_team_id=team_id)
        if status:
            queryset = queryset.filter(status=status)
        if from_date:
            queryset = queryset.filter(date__gte=from_date)
        if to_date:
            queryset = queryset.filter(date__lte=to_date)

        return queryset.distinct()


class MatchEventViewSet(viewsets.ModelViewSet):
    queryset = MatchEvent.objects.all()
    serializer_class = MatchEventSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['player__name', 'description']
    ordering_fields = ['minute', 'created_at']
    ordering = ['match', 'minute']

    def get_queryset(self):
        queryset = super().get_queryset()
        match_id = self.request.query_params.get('match')
        event_type = self.request.query_params.get('event_type')
        player_id = self.request.query_params.get('player')
        team_id = self.request.query_params.get('team')

        if match_id:
            queryset = queryset.filter(match_id=match_id)
        if event_type:
            queryset = queryset.filter(event_type=event_type)
        if player_id:
            queryset = queryset.filter(player_id=player_id)
        if team_id:
            queryset = queryset.filter(team_id=team_id)

        return queryset