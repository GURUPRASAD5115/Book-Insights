from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from .models import Book, BookChunk, BookInsight, UserQuery
from .serializers import BookSerializer, BookDetailSerializer, BookInsightSerializer, RAGQuerySerializer, UserQuerySerializer
from rag.pipeline import RAGPipeline
import logging

logger = logging.getLogger(__name__)


class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return BookDetailSerializer
        return BookSerializer

    @action(detail=True, methods=['post'])
    def process(self, request, pk=None):
        book = self.get_object()
        try:
            pipeline = RAGPipeline()
            print("🚀 Processing book:", book.id)
            pipeline.process_book(book)
            print("✅ Chunks created")
            pipeline.generate_insights(book)
            print("✅ Insights generated")
            book.processed = True
            book.save()
            return Response({'status': 'Book processed successfully'})
        except Exception as e:
            print("❌ FULL ERROR:", str(e))
            import traceback
            traceback.print_exc()
            return Response({'error': str(e)}, status=400)

    @action(detail=True, methods=['get'])
    def insights(self, request, pk=None):
        """Get insights for a specific book"""
        book = self.get_object()
        insight, created = BookInsight.objects.get_or_create(book=book)
        serializer = BookInsightSerializer(insight)
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def recommendations(self, request, pk=None):
        """Get similar books based on embeddings"""
        book = self.get_object()
        try:
            pipeline = RAGPipeline()
            similar_books = pipeline.get_recommendations(book)
            serializer = BookSerializer(similar_books, many=True)
            return Response(serializer.data)
        except Exception as e:
            logger.error(f"Error getting recommendations for {pk}: {str(e)}")
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


class BookInsightViewSet(viewsets.ModelViewSet):
    queryset = BookInsight.objects.all()
    serializer_class = BookInsightSerializer

    @action(detail=False, methods=['post'])
    def generate_insights(self, request):
        """Generate insights for all unprocessed books"""
        try:
            pipeline = RAGPipeline()
            books = Book.objects.filter(processed=False)
            for book in books:
                pipeline.generate_insights(book)
            return Response({'status': f'Generated insights for {books.count()} books'})
        except Exception as e:
            logger.error(f"Error generating insights: {str(e)}")
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


class RAGQueryView(APIView):
    """Handle RAG queries about books"""

    def post(self, request):
        serializer = RAGQuerySerializer(data=request.data)
        if serializer.is_valid():
            question = serializer.validated_data['question']
            book_ids = serializer.validated_data.get('book_ids', None)

            try:
                pipeline = RAGPipeline()
                answer, sources = pipeline.query(question, book_ids)

                # Save query to history
                user_query = UserQuery.objects.create(
                    question=question,
                    answer=answer,
                    sources=sources
                )

                return Response({
                    'question': question,
                    'answer': answer,
                    'sources': sources,
                    'query_id': user_query.id
                }, status=status.HTTP_200_OK)
            except Exception as e:
                logger.error(f"Error processing RAG query: {str(e)}")
                return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
