from django.db import models
from apps.matches.models import Match
from apps.players.models import Player
from apps.teams.models import Team

class Shot(models.Model):
    match = models.ForeignKey(Match, on_delete=models.CASCADE, related_name='shots', verbose_name='Partido')
    player = models.ForeignKey(Player, on_delete=models.CASCADE, related_name='shots', verbose_name='Jugador')
    team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='shots', verbose_name='Equipo')
    minute = models.PositiveIntegerField(verbose_name='Minuto')
    x_coordinate = models.DecimalField(max_digits=5, decimal_places=2, verbose_name='Coord X')
    y_coordinate = models.DecimalField(max_digits=5, decimal_places=2, verbose_name='Coord Y')
    distance = models.DecimalField(max_digits=6, decimal_places=2, verbose_name='Distancia (m)')
    angle = models.DecimalField(max_digits=5, decimal_places=2, verbose_name='Ángulo (°)')
    body_part = models.CharField(max_length=20, choices=[
        ('right', 'Pie Derecho'),
        ('left', 'Pie Izquierdo'),
        ('head', 'Cabeza'),
        ('other', 'Otro'),
    ], default='right', verbose_name='Parte del Cuerpo')
    situation = models.CharField(max_length=30, choices=[
        ('open_play', 'Jugada Abierta'),
        ('free_kick', 'Tiro Libre'),
        ('penalty', 'Penal'),
        ('corner', 'Córner'),
        ('cross', 'Centrada'),
    ], default='open_play', verbose_name='Situación')
    is_goal = models.BooleanField(default=False, verbose_name='Es Gol')
    xg_value = models.DecimalField(max_digits=6, decimal_places=4, default=0, verbose_name='xG')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Tiro'
        verbose_name_plural = 'Tiros'
        ordering = ['match', 'minute']

    def __str__(self):
        return f"Shot by {self.player.name} at {self.minute}'"

    @property
    def goal_proba(self):
        return float(self.xg_value)

class Pass(models.Model):
    match = models.ForeignKey(Match, on_delete=models.CASCADE, related_name='passes', verbose_name='Partido')
    from_player = models.ForeignKey(Player, on_delete=models.CASCADE, related_name='passes_made', verbose_name='De')
    to_player = models.ForeignKey(Player, on_delete=models.CASCADE, related_name='passes_received', verbose_name='A')
    team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='passes', verbose_name='Equipo')
    minute = models.PositiveIntegerField(verbose_name='Minuto')
    x_start = models.DecimalField(max_digits=5, decimal_places=2, verbose_name='X Inicio')
    y_start = models.DecimalField(max_digits=5, decimal_places=2, verbose_name='Y Inicio')
    x_end = models.DecimalField(max_digits=5, decimal_places=2, verbose_name='X Fin')
    y_end = models.DecimalField(max_digits=5, decimal_places=2, verbose_name='Y Fin')
    distance = models.DecimalField(max_digits=6, decimal_places=2, verbose_name='Distancia (m)')
    is_key_pass = models.BooleanField(default=False, verbose_name='Pase Clave')
    is_cross = models.BooleanField(default=False, verbose_name='Centrada')
    is_through_ball = models.BooleanField(default=False, verbose_name='Pase Filtrado')
    successful = models.BooleanField(verbose_name='Exitoso')
    assist = models.BooleanField(default=False, verbose_name='Asistencia')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Pase'
        verbose_name_plural = 'Pases'
        ordering = ['match', 'minute']

    def __str__(self):
        return f"{self.from_player.name} -> {self.to_player.name} at {self.minute}'"