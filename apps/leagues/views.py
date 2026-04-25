from rest_framework import viewsets, filters
from .models import League
from .serializers import LeagueSerializer
from django_filters.rest_framework import DjangoFilterBackend

class LeagueViewSet(viewsets.ModelViewSet):
    queryset = League.objects.all()
    serializer_class = LeagueSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'country', 'season']
    ordering_fields = ['name', 'country', 'season', 'created_at']
    ordering = ['-created_at']