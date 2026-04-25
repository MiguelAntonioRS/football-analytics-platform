from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ShotViewSet, PassViewSet

router = DefaultRouter()
router.register(r'shots', ShotViewSet, basename='shot')
router.register(r'passes', PassViewSet, basename='pass')

urlpatterns = [
    path('', include(router.urls)),
]