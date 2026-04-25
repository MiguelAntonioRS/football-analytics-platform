from django.contrib import admin
from .models import Match, MatchEvent

class MatchEventInline(admin.TabularInline):
    model = MatchEvent
    extra = 1

@admin.register(Match)
class MatchAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'league', 'date', 'home_score', 'away_score', 'status', 'stadium']
    list_filter = ['league', 'status', 'date']
    search_fields = ['home_team__name', 'away_team__name', 'stadium']
    inlines = [MatchEventInline]
    readonly_fields = ['created_at', 'updated_at', 'total_goals', 'events_count']

@admin.register(MatchEvent)
class MatchEventAdmin(admin.ModelAdmin):
    list_display = ['match', 'minute', 'event_type', 'player', 'team', 'is_own_goal']
    list_filter = ['event_type', 'team']
    search_fields = ['player__name', 'description']
    readonly_fields = ['created_at']