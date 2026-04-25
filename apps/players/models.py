from django.db import models
from apps.teams.models import Team
from django.conf import settings

POSITION_CHOICES = [
    ('goalkeeper', 'Portero'),
    ('defender', 'Defensa'),
    ('midfielder', 'Centrocampista'),
    ('forward', 'Delantero'),
]

class Player(models.Model):
    name = models.CharField(max_length=200, verbose_name='Nombre Completo')
    first_name = models.CharField(max_length=100, blank=True, verbose_name='Nombre')
    last_name = models.CharField(max_length=100, blank=True, verbose_name='Apellido')
    team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='players', verbose_name='Equipo')
    position = models.CharField(max_length=20, choices=POSITION_CHOICES, verbose_name='Posición')
    nationality = models.CharField(max_length=100, verbose_name='Nacionalidad')
    number = models.PositiveIntegerField(blank=True, null=True, verbose_name='Número')
    birth_date = models.DateField(blank=True, null=True, verbose_name='Fecha de Nacimiento')
    height = models.DecimalField(max_digits=4, decimal_places=2, blank=True, null=True, verbose_name='Altura (m)')
    weight = models.DecimalField(max_digits=4, decimal_places=2, blank=True, null=True, verbose_name='Peso (kg)')
    photo = models.ImageField(upload_to='players/', blank=True, null=True, verbose_name='Foto')
    is_active = models.BooleanField(default=True, verbose_name='Activo')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Jugador'
        verbose_name_plural = 'Jugadores'
        ordering = ['team', 'number', 'name']
        unique_together = ['team', 'number']

    def __str__(self):
        number_str = f" #{self.number}" if self.number else ""
        return f"{self.name}{number_str}"

    @property
    def age(self):
        from datetime import date
        if self.birth_date:
            today = date.today()
            return today.year - self.birth_date.year - (
                (today.month, today.day) < (self.birth_date.month, self.birth_date.day)
            )
        return None

    @property
    def goals_count(self):
        return self.match_events.filter(event_type='goal').count()

    @property
    def assists_count(self):
        return self.match_events.filter(event_type='assist').count()

    @property
    def yellow_cards(self):
        return self.match_events.filter(event_type='yellow_card').count()

    @property
    def red_cards(self):
        return self.match_events.filter(event_type='red_card').count()