from django.db import models

class League(models.Model):
    name = models.CharField(max_length=200, verbose_name='Nombre')
    country = models.CharField(max_length=100, verbose_name='País')
    season = models.CharField(max_length=20, verbose_name='Temporada')
    logo = models.ImageField(upload_to='leagues/', blank=True, null=True, verbose_name='Logo')
    description = models.TextField(blank=True, verbose_name='Descripción')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Liga'
        verbose_name_plural = 'Ligas'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.name} ({self.season})"

    @property
    def teams_count(self):
        return self.teams.count()

    @property
    def matches_count(self):
        return self.matches.count()

    @property
    def total_goals(self):
        from apps.matches.models import Match
        home_goals = sum(m.home_score for m in self.matches.all())
        away_goals = sum(m.away_score for m in self.matches.all())
        return home_goals + away_goals