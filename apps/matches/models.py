from django.db import models
from apps.leagues.models import League
from apps.teams.models import Team

EVENT_TYPE_CHOICES = [
    ('goal', 'Gol'),
    ('assist', 'Asistencia'),
    ('pass', 'Pase'),
    ('shot', 'Tiro'),
    ('foul', 'Falta'),
    ('yellow_card', 'Tarjeta Amarilla'),
    ('red_card', 'Tarjeta Roja'),
    ('tackle', 'Entrada'),
]

class Match(models.Model):
    STATUS_CHOICES = [
        ('scheduled', 'Programado'),
        ('in_progress', 'En Progreso'),
        ('finished', 'Finalizado'),
        ('cancelled', 'Cancelado'),
    ]

    league = models.ForeignKey(League, on_delete=models.CASCADE, related_name='matches', verbose_name='Liga')
    home_team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='home_matches', verbose_name='Equipo Local')
    away_team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='away_matches', verbose_name='Equipo Visitante')
    date = models.DateTimeField(verbose_name='Fecha y Hora')
    stadium = models.CharField(max_length=200, blank=True, verbose_name='Estadio')
    home_score = models.PositiveIntegerField(default=0, verbose_name='Goles Local')
    away_score = models.PositiveIntegerField(default=0, verbose_name='Goles Visitante')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='scheduled', verbose_name='Estado')
    round_number = models.PositiveIntegerField(blank=True, null=True, verbose_name='Jornada')
    attendance = models.PositiveIntegerField(blank=True, null=True, verbose_name='Espectadores')
    referee = models.CharField(max_length=200, blank=True, verbose_name='Árbitro')
    notes = models.TextField(blank=True, verbose_name='Notas')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Partido'
        verbose_name_plural = 'Partidos'
        ordering = ['-date']
        unique_together = ['home_team', 'away_team', 'date']

    def __str__(self):
        return f"{self.home_team} vs {self.away_team} - {self.date.strftime('%d/%m/%Y')}"

    @property
    def total_goals(self):
        return self.home_score + self.away_score

    @property
    def events_count(self):
        return self.events.count()

    @property
    def duration(self):
        from datetime import timedelta
        if self.status == 'finished':
            return 90
        return None


class MatchEvent(models.Model):
    match = models.ForeignKey(Match, on_delete=models.CASCADE, related_name='events', verbose_name='Partido')
    minute = models.PositiveIntegerField(verbose_name='Minuto')
    event_type = models.CharField(max_length=20, choices=EVENT_TYPE_CHOICES, verbose_name='Tipo de Evento')
    player = models.ForeignKey('players.Player', on_delete=models.CASCADE, related_name='match_events', verbose_name='Jugador')
    team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='match_events', verbose_name='Equipo')
    description = models.TextField(blank=True, verbose_name='Descripción')
    is_own_goal = models.BooleanField(default=False, verbose_name='Gol en Contra')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Evento del Partido'
        verbose_name_plural = 'Eventos del Partido'
        ordering = ['match', 'minute']

    def __str__(self):
        return f"{self.event_type} - {self.player.name} ({self.minute}')"