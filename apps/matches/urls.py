from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import MatchViewSet, MatchEventViewSet

router = DefaultRouter()
router.register(r'', MatchViewSet, basename='match')

event_router = DefaultRouter()
event_router.register(r'events', MatchEventViewSet, basename='match-event')

urlpatterns = [
    path('', include(router.urls)),
    path('events/', include(event_router.urls)),
]