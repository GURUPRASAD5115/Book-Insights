from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from books.views import BookViewSet, BookInsightViewSet, RAGQueryView

router = DefaultRouter()
router.register(r'books', BookViewSet, basename='book')
router.register(r'insights', BookInsightViewSet, basename='insight')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('api/rag/query/', RAGQueryView.as_view(), name='rag-query'),
]
