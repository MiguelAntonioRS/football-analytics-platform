from rest_framework import viewsets, filters
from .models import Player
from .serializers import PlayerSerializer

class PlayerViewSet(viewsets.ModelViewSet):
    queryset = Player.objects.all()
    serializer_class = PlayerSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'nationality']
    ordering_fields = ['name', 'number', 'created_at']
    ordering = ['team', 'number', 'name']

    def get_queryset(self):
        queryset = super().get_queryset()
        team_id = self.request.query_params.get('team')
        league_id = self.request.query_params.get('league')
        position = self.request.query_params.get('position')
        is_active = self.request.query_params.get('is_active')

        if team_id:
            queryset = queryset.filter(team_id=team_id)
        if league_id:
            queryset = queryset.filter(team__league_id=league_id)
        if position:
            queryset = queryset.filter(position=position)
        if is_active is not None:
            queryset = queryset.filter(is_active=is_active.lower() == 'true')

        return queryset