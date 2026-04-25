"""
URL configuration for football_analytics project.
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/leagues/', include('apps.leagues.urls')),
    path('api/teams/', include('apps.teams.urls')),
    path('api/players/', include('apps.players.urls')),
    path('api/matches/', include('apps.matches.urls')),
    path('api/events/', include('apps.events.urls')),
    path('api/analytics/', include('apps.analytics.urls')),
    path('reports/', include('apps.reports.urls')),
    path('', TemplateView.as_view(template_name='home.html'), name='home'),
    path('dashboard/', TemplateView.as_view(template_name='dashboard.html'), name='dashboard'),
    path('api-docs/', TemplateView.as_view(template_name='api_docs.html'), name='api_docs'),
    path('xg/', TemplateView.as_view(template_name='xg_analysis.html'), name='xg_analysis'),
    path('scouting/', TemplateView.as_view(template_name='scouting.html'), name='scouting'),
    path('compare/', TemplateView.as_view(template_name='player_comparison.html'), name='player_comparison'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)