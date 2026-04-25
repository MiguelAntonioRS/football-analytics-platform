from django.contrib import admin
from .models import AnalyticsData

@admin.register(AnalyticsData)
class AnalyticsDataAdmin(admin.ModelAdmin):
    list_display = ['match', 'home_possession', 'away_possession', 'home_shots', 'away_shots']
    list_filter = ['created_at']
    readonly_fields = ['created_at', 'updated_at']