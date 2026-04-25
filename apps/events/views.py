from rest_framework import viewsets, filters
from .models import Shot, Pass
from .serializers import ShotSerializer, PassSerializer

class ShotViewSet(viewsets.ModelViewSet):
    queryset = Shot.objects.all()
    serializer_class = ShotSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    ordering_fields = ['minute', 'xg_value', 'distance']
    ordering = ['match', 'minute']

    def get_queryset(self):
        queryset = super().get_queryset()
        match_id = self.request.query_params.get('match')
        player_id = self.request.query_params.get('player')
        team_id = self.request.query_params.get('team')
        is_goal = self.request.query_params.get('is_goal')

        if match_id:
            queryset = queryset.filter(match_id=match_id)
        if player_id:
            queryset = queryset.filter(player_id=player_id)
        if team_id:
            queryset = queryset.filter(team_id=team_id)
        if is_goal is not None:
            queryset = queryset.filter(is_goal=is_goal.lower() == 'true')

        return queryset

class PassViewSet(viewsets.ModelViewSet):
    queryset = Pass.objects.all()
    serializer_class = PassSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    ordering_fields = ['minute', 'distance', 'successful']
    ordering = ['match', 'minute']

    def get_queryset(self):
        queryset = super().get_queryset()
        match_id = self.request.query_params.get('match')
        player_id = self.request.query_params.get('player')
        team_id = self.request.query_params.get('team')
        from_player = self.request.query_params.get('from_player')
        to_player = self.request.query_params.get('to_player')

        if match_id:
            queryset = queryset.filter(match_id=match_id)
        if player_id:
            queryset = queryset.filter(from_player_id=player_id) | queryset.filter(to_player_id=player_id)
        if team_id:
            queryset = queryset.filter(team_id=team_id)
        if from_player:
            queryset = queryset.filter(from_player_id=from_player)
        if to_player:
            queryset = queryset.filter(to_player_id=to_player)

        return queryset