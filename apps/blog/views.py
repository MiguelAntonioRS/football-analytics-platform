from rest_framework import viewsets, status, permissions, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Category, Article, Comment, Subscription, ChatMessage
from .serializers import (
    CategorySerializer, ArticleSerializer, CommentSerializer,
    SubscriptionSerializer, ChatMessageSerializer
)


class ArticleViewSet(viewsets.ModelViewSet):
    queryset = Article.objects.filter(status='published')
    serializer_class = ArticleSerializer
    lookup_field = 'slug'
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['title', 'content']
    ordering = ['-created_at']

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [permissions.IsAuthenticated()]
        return [permissions.AllowAny()]

    @action(detail=True, methods=['post'])
    def like(self, request, slug=None):
        article = self.get_object()
        if request.user in article.likes.all():
            article.likes.remove(request.user)
            return Response({'status': 'unliked'})
        else:
            article.likes.add(request.user)
            return Response({'status': 'liked'})

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer

    def get_queryset(self):
        return Comment.objects.filter(parent=None)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class SubscriptionViewSet(viewsets.ModelViewSet):
    serializer_class = SubscriptionSerializer

    def get_queryset(self):
        return Subscription.objects.filter(user=self.request.user)

    @action(detail=False, methods=['post'])
    def subscribe(self, request):
        plan = request.data.get('plan', 'free')
        subscription, created = Subscription.objects.update_or_create(
            user=request.user,
            defaults={'plan': plan, 'is_active': True}
        )
        return Response(SubscriptionSerializer(subscription).data)


class ChatMessageViewSet(viewsets.ModelViewSet):
    serializer_class = ChatMessageSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return ChatMessage.objects.all().order_by('-created_at')[:100]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)