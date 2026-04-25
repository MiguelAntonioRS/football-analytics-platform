from django.urls import path
from .views import (
    TeamComparisonView, PlayerComparisonView, LeagueStandingsView,
    GoalsByPlayerView, GoalsByTeamView
)

urlpatterns = [
    path('team-comparison/', TeamComparisonView.as_view(), name='team-comparison'),
    path('player-comparison/', PlayerComparisonView.as_view(), name='player-comparison'),
    path('standings/<int:league_id>/', LeagueStandingsView.as_view(), name='league-standings'),
    path('goals-by-player/', GoalsByPlayerView.as_view(), name='goals-by-player'),
    path('goals-by-team/', GoalsByTeamView.as_view(), name='goals-by-team'),
]