from django.db import models
from django.conf import settings


class FantasyTeam(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='fantasy_team')
    name = models.CharField(max_length=100)
    budget = models.DecimalField(max_digits=10, decimal_places=2, default=100000000)
    points = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Equipo Fantasy'
        verbose_name_plural = 'Equipos Fantasy'

    def __str__(self):
        return f"{self.user.username} - {self.name}"


class FantasyPlayer(models.Model):
    POSITION_CHOICES = [
        ('GK', 'Portero'),
        ('DEF', 'Defensa'),
        ('MID', 'Centrocampista'),
        ('FWD', 'Delantero'),
    ]

    real_player = models.ForeignKey('players.Player', on_delete=models.CASCADE, related_name='fantasy_versions')
    fantasy_team = models.ForeignKey(FantasyTeam, on_delete=models.CASCADE, related_name='players')
    position = models.CharField(max_length=3, choices=POSITION_CHOICES)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    is_captain = models.BooleanField(default=False)
    is_vice_captain = models.BooleanField(default=False)
    is_bench = models.BooleanField(default=False)

    class Meta:
        unique_together = ['real_player', 'fantasy_team']
        verbose_name = 'Jugador Fantasy'
        verbose_name_plural = 'Jugadores Fantasy'

    def __str__(self):
        return f"{self.real_player.name} - {self.position}"


class Gameweek(models.Model):
    number = models.PositiveIntegerField(unique=True)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    is_active = models.BooleanField(default=True)
    deadline = models.DateTimeField()

    class Meta:
        verbose_name = 'Jornada'
        verbose_name_plural = 'Jornadas'
        ordering = ['number']

    def __str__(self):
        return f"Jornada {self.number}"


class Prediction(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='predictions')
    match = models.ForeignKey('matches.Match', on_delete=models.CASCADE, related_name='predictions')
    home_score = models.PositiveIntegerField()
    away_score = models.PositiveIntegerField()
    points = models.PositiveIntegerField(default=0)
    is_correct = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['user', 'match']
        verbose_name = 'Predicción'
        verbose_name_plural = 'Predicciones'

    def __str__(self):
        return f"{self.user.username}: {self.home_score}-{self.away_score}"


class Achievement(models.Model):
    CATEGORY_CHOICES = [
        ('scoring', 'Goles'),
        ('prediction', 'Predicciones'),
        ('fantasy', 'Fantasy'),
        ('social', 'Social'),
        ('streak', 'Racha'),
    ]

    name = models.CharField(max_length=100)
    description = models.TextField()
    icon = models.CharField(max_length=50, default='🏆')
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    requirement = models.PositiveIntegerField()
    points_reward = models.PositiveIntegerField(default=10)

    class Meta:
        verbose_name = 'Logro'
        verbose_name_plural = 'Logros'

    def __str__(self):
        return self.name


class UserAchievement(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='achievements')
    achievement = models.ForeignKey(Achievement, on_delete=models.CASCADE)
    earned_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['user', 'achievement']
        verbose_name = 'Logro de Usuario'
        verbose_name_plural = 'Logros de Usuario'


class Leaderboard(models.Model):
    PERIOD_CHOICES = [
        ('weekly', 'Semanal'),
        ('monthly', 'Mensual'),
        ('all_time', 'Histórico'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='leaderboard_entries')
    points = models.PositiveIntegerField(default=0)
    period = models.CharField(max_length=20, choices=PERIOD_CHOICES, default='weekly')
    rank = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Clasificación'
        verbose_name_plural = 'Clasificaciones'
        unique_together = ['user', 'period']


class Quiz(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    question_count = models.PositiveIntegerField(default=5)
    points_per_question = models.PositiveIntegerField(default=10)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class QuizQuestion(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='questions')
    question = models.TextField()
    option_a = models.CharField(max_length=200)
    option_b = models.CharField(max_length=200)
    option_c = models.CharField(max_length=200)
    option_d = models.CharField(max_length=200)
    correct_answer = models.CharField(max_length=1)

    def __str__(self):
        return self.question[:50]