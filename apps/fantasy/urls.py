from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import FantasyTeamViewSet, PredictionViewSet, AchievementViewSet, LeaderboardViewSet, QuizViewSet

router = DefaultRouter()
router.register(r'fantasy-team', FantasyTeamViewSet, basename='fantasy-team')
router.register(r'predictions', PredictionViewSet, basename='prediction')
router.register(r'achievements', AchievementViewSet, basename='achievement')
router.register(r'leaderboard', LeaderboardViewSet, basename='leaderboard')
router.register(r'quizzes', QuizViewSet, basename='quiz')

urlpatterns = [
    path('', include(router.urls)),
]