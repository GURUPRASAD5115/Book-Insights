from rest_framework import serializers
from .models import Book, BookChunk, BookInsight, UserQuery, ChatHistory


class BookChunkSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookChunk
        fields = ['id', 'text', 'chunk_index']


class BookInsightSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookInsight
        fields = ['id', 'book', 'summary', 'genres', 'sentiment', 'recommendations', 'created_at', 'updated_at']


class BookSerializer(serializers.ModelSerializer):
    chunks = BookChunkSerializer(many=True, read_only=True)
    insight = BookInsightSerializer(read_only=True)

    class Meta:
        model = Book
        fields = ['id', 'title', 'author', 'description', 'rating', 'url', 'cover_image', 'uploaded_at', 'processed', 'chunks', 'insight']


class BookDetailSerializer(serializers.ModelSerializer):
    chunks = BookChunkSerializer(many=True, read_only=True)
    insight = BookInsightSerializer(read_only=True)

    class Meta:
        model = Book
        fields = ['id', 'title', 'author', 'description', 'rating', 'url', 'cover_image', 'uploaded_at', 'processed', 'chunks', 'insight']


class RAGQuerySerializer(serializers.Serializer):
    question = serializers.CharField(max_length=1000)
    book_ids = serializers.ListField(child=serializers.IntegerField(), required=False)


class UserQuerySerializer(serializers.ModelSerializer):
    class Meta:
        model = UserQuery
        fields = ['id', 'question', 'answer', 'sources', 'created_at']


class ChatHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ChatHistory
        fields = ['id', 'user_id', 'messages', 'created_at', 'updated_at']
