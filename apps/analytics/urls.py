from django.urls import path
from .views import (
    TeamStatisticsView, PlayerStatisticsView, TopScorersView, TopAssistsView,
    LeagueStatisticsView, MatchEventsSummaryView, SeasonStatisticsView,
    DashboardDataView
)

urlpatterns = [
    path('teams/<int:team_id>/', TeamStatisticsView.as_view(), name='team-statistics'),
    path('players/<int:player_id>/', PlayerStatisticsView.as_view(), name='player-statistics'),
    path('scorers/', TopScorersView.as_view(), name='top-scorers'),
    path('assists/', TopAssistsView.as_view(), name='top-assists'),
    path('leagues/<int:league_id>/', LeagueStatisticsView.as_view(), name='league-statistics'),
    path('matches/<int:match_id>/summary/', MatchEventsSummaryView.as_view(), name='match-events-summary'),
    path('seasons/<str:season>/', SeasonStatisticsView.as_view(), name='season-statistics'),
    path('dashboard/', DashboardDataView.as_view(), name='dashboard-data'),
]