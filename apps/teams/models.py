from django.db import models
from apps.leagues.models import League

class Team(models.Model):
    name = models.CharField(max_length=200, verbose_name='Nombre')
    league = models.ForeignKey(League, on_delete=models.CASCADE, related_name='teams', verbose_name='Liga')
    stadium = models.CharField(max_length=200, verbose_name='Estadio')
    coach = models.CharField(max_length=200, verbose_name='Entrenador')
    logo = models.ImageField(upload_to='teams/', blank=True, null=True, verbose_name='Logo')
    founded_year = models.PositiveIntegerField(blank=True, null=True, verbose_name='Año de Fundación')
    website = models.URLField(blank=True, null=True, verbose_name='Sitio Web')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Equipo'
        verbose_name_plural = 'Equipos'
        ordering = ['name']
        unique_together = ['name', 'league']

    def __str__(self):
        return self.name

    @property
    def players_count(self):
        return self.players.count()

    @property
    def home_matches_count(self):
        return self.home_matches.count()

    @property
    def away_matches_count(self):
        return self.away_matches.count()

    @property
    def total_matches(self):
        return self.home_matches_count + self.away_matches_count