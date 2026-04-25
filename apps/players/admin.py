from django.contrib import admin
from .models import Player

@admin.register(Player)
class PlayerAdmin(admin.ModelAdmin):
    list_display = ['name', 'team', 'position', 'number', 'nationality', 'age', 'goals_count', 'assists_count']
    list_filter = ['team__league', 'team', 'position', 'nationality']
    search_fields = ['name', 'nationality']
    readonly_fields = ['created_at', 'updated_at', 'age', 'goals_count', 'assists_count', 'yellow_cards', 'red_cards']