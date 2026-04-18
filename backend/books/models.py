from django.db import models
from django.contrib.postgres.fields import ArrayField
import json


class Book(models.Model):
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    description = models.TextField()
    rating = models.FloatField(default=0.0)
    url = models.URLField(blank=True, null=True)
    cover_image = models.URLField(blank=True, null=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    processed = models.BooleanField(default=False)

    class Meta:
        ordering = ['-uploaded_at']

    def __str__(self):
        return self.title


class BookChunk(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='chunks')
    text = models.TextField()
    embedding = models.JSONField(default=list)
    chunk_index = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['chunk_index']
        unique_together = ('book', 'chunk_index')

    def __str__(self):
        return f"Chunk {self.chunk_index} of {self.book.title}"


class BookInsight(models.Model):
    INSIGHT_TYPES = (
        ('summary', 'Summary'),
        ('genre', 'Genre Classification'),
        ('sentiment', 'Sentiment Analysis'),
        ('recommendation', 'Recommendation'),
    )

    book = models.OneToOneField(Book, on_delete=models.CASCADE, related_name='insight')
    summary = models.TextField(blank=True, null=True)
    genres = models.JSONField(default=list)  # List of genres
    sentiment = models.CharField(max_length=50, blank=True, null=True)
    recommendations = models.JSONField(default=list)  # List of similar book IDs
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Insight for {self.book.title}"


class UserQuery(models.Model):
    question = models.TextField()
    answer = models.TextField()
    sources = models.JSONField(default=list)  # List of book IDs used as context
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Query: {self.question[:50]}..."


class ChatHistory(models.Model):
    user_id = models.CharField(max_length=100, default='anonymous')
    messages = models.JSONField(default=list)  # Store chat messages as JSON
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-updated_at']

    def __str__(self):
        return f"Chat for {self.user_id}"
