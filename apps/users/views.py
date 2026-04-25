from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView
from django.contrib.auth import get_user_model
from django.db.models import Q
from .models import FavoriteTeam, FavoritePlayer, Notification, Comment
from .serializers import (
    UserSerializer, UserRegistrationSerializer,
    FavoriteTeamSerializer, FavoritePlayerSerializer,
    NotificationSerializer, CommentSerializer
)

User = get_user_model()


class RegisterView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({
                'message': 'Usuario registrado exitosamente',
                'user': UserSerializer(user).data
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserProfileView(APIView):
    def get(self, request, user_id=None):
        if user_id:
            user = User.objects.get(id=user_id)
        else:
            user = request.user
        serializer = UserSerializer(user)
        return Response(serializer.data)

    def put(self, request):
        if not request.user.is_authenticated:
            return Response({'error': 'No autenticado'}, status=status.HTTP_401_UNAUTHORIZED)
        serializer = UserSerializer(request.user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class FavoriteTeamViewSet(viewsets.ModelViewSet):
    serializer_class = FavoriteTeamSerializer

    def get_queryset(self):
        return FavoriteTeam.objects.filter(user=self.request.user)

    @action(detail=False, methods=['get'])
    def check(self, request):
        team_id = request.query_params.get('team_id')
        if team_id:
            exists = FavoriteTeam.objects.filter(user=request.user, team_id=team_id).exists()
            return Response({'is_favorite': exists})
        return Response({'error': 'team_id required'})

    @action(detail=False, methods=['post'])
    def toggle(self, request):
        team_id = request.data.get('team_id')
        if not team_id:
            return Response({'error': 'team_id required'}, status=status.HTTP_400_BAD_REQUEST)

        favorite, created = FavoriteTeam.objects.get_or_create(
            user=request.user,
            team_id=team_id
        )
        if not created:
            favorite.delete()
            return Response({'status': 'removed'})
        return Response({'status': 'added'})


class FavoritePlayerViewSet(viewsets.ModelViewSet):
    serializer_class = FavoritePlayerSerializer

    def get_queryset(self):
        return FavoritePlayer.objects.filter(user=self.request.user)

    @action(detail=False, methods=['get'])
    def check(self, request):
        player_id = request.query_params.get('player_id')
        if player_id:
            exists = FavoritePlayer.objects.filter(user=request.user, player_id=player_id).exists()
            return Response({'is_favorite': exists})
        return Response({'error': 'player_id required'})

    @action(detail=False, methods=['post'])
    def toggle(self, request):
        player_id = request.data.get('player_id')
        if not player_id:
            return Response({'error': 'player_id required'}, status=status.HTTP_400_BAD_REQUEST)

        favorite, created = FavoritePlayer.objects.get_or_create(
            user=request.user,
            player_id=player_id
        )
        if not created:
            favorite.delete()
            return Response({'status': 'removed'})
        return Response({'status': 'added'})


class NotificationViewSet(viewsets.ModelViewSet):
    serializer_class = NotificationSerializer

    def get_queryset(self):
        return Notification.objects.filter(user=self.request.user)

    @action(detail=False, methods=['post'])
    def mark_all_read(self, request):
        self.request.user.notifications.filter(is_read=False).update(is_read=True)
        return Response({'status': 'all marked as read'})

    @action(detail=True, methods=['post'])
    def mark_read(self, request, pk=None):
        notification = self.get_object()
        notification.is_read = True
        notification.save()
        return Response({'status': 'marked as read'})


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer

    def get_queryset(self):
        queryset = Comment.objects.filter(parent=None)
        match_id = self.request.query_params.get('match')
        if match_id:
            queryset = queryset.filter(match_id=match_id)
        return queryset

    @action(detail=True, methods=['post'])
    def like(self, request, pk=None):
        comment = self.get_object()
        if request.user in comment.likes.all():
            comment.likes.remove(request.user)
            return Response({'status': 'unliked', 'likes_count': comment.like_count})
        else:
            comment.likes.add(request.user)
            return Response({'status': 'liked', 'likes_count': comment.like_count})

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)