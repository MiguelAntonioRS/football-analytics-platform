from django.contrib import admin
from .models import Team

@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = ['name', 'league', 'stadium', 'coach', 'players_count', 'created_at']
    list_filter = ['league']
    search_fields = ['name', 'stadium', 'coach']
    readonly_fields = ['created_at', 'updated_at']