from rest_framework import viewsets, filters
from .models import Team
from .serializers import TeamSerializer

class TeamViewSet(viewsets.ModelViewSet):
    queryset = Team.objects.all()
    serializer_class = TeamSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'stadium', 'coach']
    ordering_fields = ['name', 'created_at']
    ordering = ['name']