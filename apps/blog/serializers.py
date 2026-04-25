from rest_framework import serializers, filters
from .models import Category, Article, Comment, Subscription, ChatMessage


class CategorySerializer(serializers.ModelSerializer):
    article_count = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = ['id', 'name', 'slug', 'description', 'article_count']

    def get_article_count(self, obj):
        return obj.articles.filter(status='published').count()


class CommentSerializer(serializers.ModelSerializer):
    author_name = serializers.CharField(source='author.username', read_only=True)
    author_avatar = serializers.ImageField(source='author.avatar', read_only=True)
    replies = serializers.SerializerMethodField()
    reply_count = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = ['id', 'article', 'author', 'author_name', 'author_avatar', 'content', 'parent', 'reply_count', 'replies', 'created_at']

    def get_replies(self, obj):
        if obj.parent is None:
            return CommentSerializer(obj.replies.all(), many=True).data
        return []

    def get_reply_count(self, obj):
        return obj.replies.count()


class ArticleSerializer(serializers.ModelSerializer):
    author_name = serializers.CharField(source='author.username', read_only=True)
    category_name = serializers.CharField(source='category.name', read_only=True)
    like_count = serializers.IntegerField(read_only=True)
    is_liked = serializers.SerializerMethodField()
    comment_count = serializers.SerializerMethodField()

    class Meta:
        model = Article
        fields = ['id', 'author', 'author_name', 'title', 'slug', 'category', 'category_name', 'image', 'excerpt', 'content', 'status', 'views', 'like_count', 'is_liked', 'comment_count', 'created_at', 'updated_at']
        read_only_fields = ['views', 'created_at', 'updated_at']

    def get_is_liked(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return request.user in obj.likes.all()
        return False

    def get_comment_count(self, obj):
        return obj.comments.count()


class SubscriptionSerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(source='user.username', read_only=True)

    class Meta:
        model = Subscription
        fields = ['id', 'user', 'user_name', 'plan', 'start_date', 'end_date', 'is_active']


class ChatMessageSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)
    user_avatar = serializers.ImageField(source='user.avatar', read_only=True)

    class Meta:
        model = ChatMessage
        fields = ['id', 'user', 'username', 'user_avatar', 'content', 'created_at']