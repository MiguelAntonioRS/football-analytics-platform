from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, FavoriteTeam, FavoritePlayer, Notification, Comment

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ['username', 'email', 'is_premium', 'is_staff', 'created_at']
    list_filter = ['is_premium', 'is_staff', 'is_active']
    search_fields = ['username', 'email']
    fieldsets = UserAdmin.fieldsets + (
        ('Extra Info', {'fields': ('avatar', 'bio', 'country', 'is_premium')}),
    )

@admin.register(FavoriteTeam)
class FavoriteTeamAdmin(admin.ModelAdmin):
    list_display = ['user', 'team', 'created_at']
    list_filter = ['created_at']
    search_fields = ['user__username', 'team__name']

@admin.register(FavoritePlayer)
class FavoritePlayerAdmin(admin.ModelAdmin):
    list_display = ['user', 'player', 'created_at']
    list_filter = ['created_at']
    search_fields = ['user__username', 'player__name']

@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ['user', 'type', 'title', 'is_read', 'created_at']
    list_filter = ['type', 'is_read', 'created_at']
    search_fields = ['user__username', 'title', 'message']

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['user', 'match', 'content', 'like_count', 'reply_count', 'created_at']
    list_filter = ['created_at']
    search_fields = ['user__username', 'content']