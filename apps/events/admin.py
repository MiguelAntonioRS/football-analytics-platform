from django.contrib import admin
from .models import Shot, Pass

@admin.register(Shot)
class ShotAdmin(admin.ModelAdmin):
    list_display = ['player', 'team', 'minute', 'distance', 'is_goal', 'xg_value']
    list_filter = ['is_goal', 'body_part', 'situation', 'team']
    search_fields = ['player__name']
    readonly_fields = ['created_at']

@admin.register(Pass)
class PassAdmin(admin.ModelAdmin):
    list_display = ['from_player', 'to_player', 'team', 'minute', 'successful', 'is_key_pass']
    list_filter = ['successful', 'is_key_pass', 'is_cross', 'team']
    search_fields = ['from_player__name', 'to_player__name']
    readonly_fields = ['created_at']