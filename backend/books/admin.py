from django.contrib import admin
from .models import Book, BookChunk, BookInsight, UserQuery, ChatHistory


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'rating', 'processed', 'uploaded_at')
    list_filter = ('processed', 'uploaded_at')
    search_fields = ('title', 'author')
    readonly_fields = ('uploaded_at',)


@admin.register(BookChunk)
class BookChunkAdmin(admin.ModelAdmin):
    list_display = ('book', 'chunk_index')
    list_filter = ('book',)
    search_fields = ('book__title', 'text')


@admin.register(BookInsight)
class BookInsightAdmin(admin.ModelAdmin):
    list_display = ('book', 'created_at', 'updated_at')
    list_filter = ('created_at',)
    search_fields = ('book__title',)
    readonly_fields = ('created_at', 'updated_at')


@admin.register(UserQuery)
class UserQueryAdmin(admin.ModelAdmin):
    list_display = ('question', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('question', 'answer')
    readonly_fields = ('created_at',)


@admin.register(ChatHistory)
class ChatHistoryAdmin(admin.ModelAdmin):
    list_display = ('user_id', 'created_at', 'updated_at')
    list_filter = ('created_at', 'user_id')
    readonly_fields = ('created_at', 'updated_at')
