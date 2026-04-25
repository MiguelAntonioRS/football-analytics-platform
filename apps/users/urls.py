from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import (
    RegisterView, UserProfileView,
    FavoriteTeamViewSet, FavoritePlayerViewSet,
    NotificationViewSet, CommentViewSet
)

router = DefaultRouter()
router.register(r'favorites/teams', FavoriteTeamViewSet, basename='favorite-team')
router.register(r'favorites/players', FavoritePlayerViewSet, basename='favorite-player')
router.register(r'notifications', NotificationViewSet, basename='notification')
router.register(r'comments', CommentViewSet, basename='comment')

urlpatterns = [
    path('auth/register/', RegisterView.as_view(), name='register'),
    path('auth/login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('profile/', UserProfileView.as_view(), name='user-profile'),
    path('profile/<int:user_id>/', UserProfileView.as_view(), name='user-profile-detail'),
    path('', include(router.urls)),
]