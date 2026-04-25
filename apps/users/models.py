from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models import ManyToManyField


class User(AbstractUser):
    email = models.EmailField(unique=True)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    bio = models.TextField(blank=True, max_length=500)
    country = models.CharField(max_length=100, blank=True)
    is_premium = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    class Meta:
        verbose_name = 'Usuario'
        verbose_name_plural = 'Usuarios'

    def __str__(self):
        return self.email

    @property
    def favorite_teams(self):
        return self.favorite_teams.all()

    @property
    def favorite_players(self):
        return self.favorite_players.all()


class FavoriteTeam(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='favorite_team_entries')
    team = models.ForeignKey('teams.Team', on_delete=models.CASCADE, related_name='fans')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['user', 'team']
        verbose_name = 'Equipo Favorito'
        verbose_name_plural = 'Equipos Favoritos'

    def __str__(self):
        return f"{self.user.username} - {self.team.name}"


class FavoritePlayer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='favorite_player_entries')
    player = models.ForeignKey('players.Player', on_delete=models.CASCADE, related_name='followers')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['user', 'player']
        verbose_name = 'Jugador Favorito'
        verbose_name_plural = 'Jugadores Favoritos'

    def __str__(self):
        return f"{self.user.username} - {self.player.name}"


class Notification(models.Model):
    TYPE_CHOICES = [
        ('match', 'Nuevo Partido'),
        ('goal', 'Gol'),
        ('team_news', 'Noticias del Equipo'),
        ('player_news', 'Noticias del Jugador'),
        ('system', 'Sistema'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    title = models.CharField(max_length=200)
    message = models.TextField()
    link = models.CharField(max_length=500, blank=True)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Notificación'
        verbose_name_plural = 'Notificaciones'

    def __str__(self):
        return f"{self.user.username} - {self.title}"


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    match = models.ForeignKey('matches.Match', on_delete=models.CASCADE, related_name='comments', null=True, blank=True)
    content = models.TextField(max_length=1000)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='replies')
    likes = models.ManyToManyField(User, related_name='liked_comments', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Comentario'
        verbose_name_plural = 'Comentarios'

    def __str__(self):
        return f"{self.user.username}: {self.content[:50]}"

    @property
    def reply_count(self):
        return self.replies.count()

    @property
    def like_count(self):
        return self.likes.count()