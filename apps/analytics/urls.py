from django.urls import path
from .views import (
    TeamStatisticsView, PlayerStatisticsView, TopScorersView, TopAssistsView,
    LeagueStatisticsView, MatchEventsSummaryView, SeasonStatisticsView,
    DashboardDataView
)
from .views_advanced import (
    PassNetworkView, ShotMapView, PredictionView, RankingView, ScoutingView,
    XGAnalysisView, PlayerComparisonView, TeamFormView, LeagueTableView
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
    path('pass-network/<int:match_id>/<int:team_id>/', PassNetworkView.as_view(), name='pass-network'),
    path('shot-map/<int:match_id>/', ShotMapView.as_view(), name='shot-map'),
    path('prediction/<int:home_team_id>/<int:away_team_id>/<int:league_id>/', PredictionView.as_view(), name='prediction'),
    path('ranking/', RankingView.as_view(), name='ranking'),
    path('scouting/', ScoutingView.as_view(), name='scouting'),
    path('xg/', XGAnalysisView.as_view(), name='xg-analysis'),
    path('top-xg/', XGAnalysisView.as_view(), name='top-xg'),
    path('player-comparison/', PlayerComparisonView.as_view(), name='player-comparison'),
    path('team-form/<int:team_id>/', TeamFormView.as_view(), name='team-form'),
    path('standings/<int:league_id>/', LeagueTableView.as_view(), name='standings'),
]