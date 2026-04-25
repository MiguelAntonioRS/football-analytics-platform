from rest_framework import serializers, filters
from django.contrib.auth import get_user_model
from .models import FavoriteTeam, FavoritePlayer, Notification, Comment

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    favorite_teams_count = serializers.SerializerMethodField()
    favorite_players_count = serializers.SerializerMethodField()
    unread_notifications = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = [
            'id', 'username', 'email', 'avatar', 'bio', 'country',
            'is_premium', 'favorite_teams_count', 'favorite_players_count',
            'unread_notifications', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'is_premium', 'created_at', 'updated_at']

    def get_favorite_teams_count(self, obj):
        return obj.favorite_team_entries.count()

    def get_favorite_players_count(self, obj):
        return obj.favorite_player_entries.count()

    def get_unread_notifications(self, obj):
        return obj.notifications.filter(is_read=False).count()


class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)
    password_confirm = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'password_confirm', 'first_name', 'last_name']

    def validate(self, data):
        if data['password'] != data['password_confirm']:
            raise serializers.ValidationError({'password_confirm': 'Las contraseñas no coinciden'})
        return data

    def create(self, validated_data):
        validated_data.pop('password_confirm')
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user


class FavoriteTeamSerializer(serializers.ModelSerializer):
    team_name = serializers.CharField(source='team.name', read_only=True)
    team_logo = serializers.ImageField(source='team.logo', read_only=True)

    class Meta:
        model = FavoriteTeam
        fields = ['id', 'team', 'team_name', 'team_logo', 'created_at']
        read_only_fields = ['user', 'created_at']


class FavoritePlayerSerializer(serializers.ModelSerializer):
    player_name = serializers.CharField(source='player.name', read_only=True)
    player_photo = serializers.ImageField(source='player.photo', read_only=True)
    player_team = serializers.CharField(source='player.team.name', read_only=True)

    class Meta:
        model = FavoritePlayer
        fields = ['id', 'player', 'player_name', 'player_photo', 'player_team', 'created_at']
        read_only_fields = ['user', 'created_at']


class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = ['id', 'type', 'title', 'message', 'link', 'is_read', 'created_at']
        read_only_fields = ['user', 'type', 'title', 'message', 'link', 'created_at']


class CommentSerializer(serializers.ModelSerializer):
    user_username = serializers.CharField(source='user.username', read_only=True)
    user_avatar = serializers.ImageField(source='user.avatar', read_only=True)
    reply_count = serializers.IntegerField(read_only=True)
    like_count = serializers.IntegerField(read_only=True)
    is_liked = serializers.SerializerMethodField()
    replies = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = [
            'id', 'user', 'user_username', 'user_avatar', 'match', 'content',
            'parent', 'reply_count', 'like_count', 'is_liked', 'replies',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['user', 'created_at', 'updated_at']

    def get_is_liked(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return request.user in obj.likes.all()
        return False

    def get_replies(self, obj):
        if obj.parent is None:
            return CommentSerializer(obj.replies.all(), many=True, context=self.context).data
        return []