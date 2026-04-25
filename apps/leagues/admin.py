from django.contrib import admin
from .models import League

@admin.register(League)
class LeagueAdmin(admin.ModelAdmin):
    list_display = ['name', 'country', 'season', 'teams_count', 'matches_count', 'created_at']
    list_filter = ['country', 'season']
    search_fields = ['name', 'country']
    readonly_fields = ['created_at', 'updated_at']