from django.contrib import admin
from .models import FantasyTeam, FantasyPlayer, Gameweek, Prediction, Achievement, UserAchievement, Leaderboard, Quiz, QuizQuestion


@admin.register(FantasyTeam)
class FantasyTeamAdmin(admin.ModelAdmin):
    list_display = ['user', 'name', 'budget', 'points', 'created_at']
    list_filter = ['created_at']


@admin.register(Gameweek)
class GameweekAdmin(admin.ModelAdmin):
    list_display = ['number', 'start_date', 'end_date', 'is_active', 'deadline']
    list_filter = ['is_active']


@admin.register(Prediction)
class PredictionAdmin(admin.ModelAdmin):
    list_display = ['user', 'match', 'home_score', 'away_score', 'points', 'is_correct']
    list_filter = ['is_correct']


@admin.register(Achievement)
class AchievementAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'requirement', 'points_reward']
    list_filter = ['category']


@admin.register(Quiz)
class QuizAdmin(admin.ModelAdmin):
    list_display = ['title', 'question_count', 'is_active']


@admin.register(QuizQuestion)
class QuizQuestionAdmin(admin.ModelAdmin):
    list_display = ['quiz', 'question', 'correct_answer']