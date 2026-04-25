from django.db import models

class AnalyticsData(models.Model):
    match = models.OneToOneField('matches.Match', on_delete=models.CASCADE, related_name='analytics', verbose_name='Partido')
    home_possession = models.DecimalField(max_digits=5, decimal_places=2, default=50, verbose_name='Posesión Local %')
    away_possession = models.DecimalField(max_digits=5, decimal_places=2, default=50, verbose_name='Posesión Visitante %')
    home_shots = models.PositiveIntegerField(default=0, verbose_name='Tiros Local')
    away_shots = models.PositiveIntegerField(default=0, verbose_name='Tiros Visitante')
    home_shots_on_target = models.PositiveIntegerField(default=0, verbose_name='Tiros a Puerta Local')
    away_shots_on_target = models.PositiveIntegerField(default=0, verbose_name='Tiros a Puerta Visitante')
    home_passes = models.PositiveIntegerField(default=0, verbose_name='Pases Local')
    away_passes = models.PositiveIntegerField(default=0, verbose_name='Pases Visitante')
    home_pass_accuracy = models.DecimalField(max_digits=5, decimal_places=2, default=0, verbose_name='Precisión de Pases Local %')
    away_pass_accuracy = models.DecimalField(max_digits=5, decimal_places=2, default=0, verbose_name='Precisión de Pases Visitante %')
    home_fouls = models.PositiveIntegerField(default=0, verbose_name='Faltas Local')
    away_fouls = models.PositiveIntegerField(default=0, verbose_name='Faltas Visitante')
    home_corners = models.PositiveIntegerField(default=0, verbose_name='Córners Local')
    away_corners = models.PositiveIntegerField(default=0, verbose_name='Córners Visitante')
    home_yellow_cards = models.PositiveIntegerField(default=0, verbose_name='Tarjetas Amarillas Local')
    away_yellow_cards = models.PositiveIntegerField(default=0, verbose_name='Tarjetas Amarillas Visitante')
    home_red_cards = models.PositiveIntegerField(default=0, verbose_name='Tarjetas Rojas Local')
    away_red_cards = models.PositiveIntegerField(default=0, verbose_name='Tarjetas Rojas Visitante')
    home_offsides = models.PositiveIntegerField(default=0, verbose_name='Fuera de Lugar Local')
    away_offsides = models.PositiveIntegerField(default=0, verbose_name='Fuera de Lugar Visitante')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Dato Analítico'
        verbose_name_plural = 'Datos Analíticos'

    def __str__(self):
        return f"Analytics - {self.match}"