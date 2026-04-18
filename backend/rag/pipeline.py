from books.models import Book, BookChunk, BookInsight
from .embeddings import EmbeddingManager
from .llm import LLMManager
import logging

logger = logging.getLogger(__name__)


class RAGPipeline:
    def __init__(self):
        self.embedding_manager = EmbeddingManager()

        try:
            self.llm_manager = LLMManager()
        except Exception as e:
            logger.warning(f"LLM not available: {str(e)}")
            self.llm_manager = None

    # -------------------------------
    # CHUNKING
    # -------------------------------
    def chunk_text(self, text, chunk_size=400, overlap=80):
        chunks = []
        step = chunk_size - overlap

        for i in range(0, len(text), step):
            chunk = text[i:i + chunk_size]
            if chunk.strip():
                chunks.append(chunk)

        return chunks

    # -------------------------------
    # PROCESS BOOK
    # -------------------------------
    def process_book(self, book):
        try:
            if not book.description:
                raise Exception("Book description empty")

            BookChunk.objects.filter(book=book).delete()

            chunks = self.chunk_text(book.description)

            for idx, chunk_text in enumerate(chunks):
                try:
                    embedding = self.embedding_manager.embed_text(chunk_text)
                except:
                    embedding = [0.0] * 10

                BookChunk.objects.create(
                    book=book,
                    text=chunk_text,
                    embedding=embedding,
                    chunk_index=idx
                )

            print(f"✅ Book {book.id} processed")

            self.generate_insights(book)

        except Exception as e:
            print("❌ PROCESS ERROR:", str(e))
            raise

    # -------------------------------
    # INSIGHTS
    # -------------------------------
    def generate_insights(self, book):
        try:
            insight, _ = BookInsight.objects.get_or_create(book=book)

            if self.llm_manager:
                insight.summary = self.llm_manager.generate_summary(book.description)
                insight.genres = self.llm_manager.classify_genres(book.description)
                insight.sentiment = self.llm_manager.analyze_sentiment(book.description)
            else:
                insight.summary = book.description[:200]
                insight.genres = ["Fiction"]
                insight.sentiment = "Neutral"

            insight.save()
            print("✅ Insights saved")

        except Exception as e:
            print("❌ INSIGHT ERROR:", str(e))

    # -------------------------------
    # 🔥 SMART RAG QUERY
    # -------------------------------
    def query(self, question, book_ids=None):
        try:
            chunks = (
                BookChunk.objects.filter(book_id__in=book_ids)
                if book_ids else BookChunk.objects.all()
            )

            if not chunks.exists():
                return "No data available", []

            # 🔹 Step 1: embed question
            query_embedding = self.embedding_manager.embed_text(question)

            scored = []

            for chunk in chunks:
                try:
                    score = self.embedding_manager.similarity(
                        query_embedding,
                        chunk.embedding
                    )
                    scored.append((score, chunk.text))
                except:
                    continue

            # 🔹 Step 2: sort
            scored.sort(reverse=True, key=lambda x: x[0])

            # 🔹 Step 3: filter relevant chunks
            filtered = [c for c in scored if c[0] > 0.25]

            if not filtered:
                return "Not enough relevant information", []

            # 🔹 Step 4: top chunks
            top_chunks = [text[:300] for _, text in filtered[:3]]

            # 🔹 Step 5: structured context
            context = "\n\n---\n\n".join([
                f"Chunk {i+1}: {t}" for i, t in enumerate(top_chunks)
            ])

            # 🔹 Step 6: ask LLM
            if self.llm_manager:
                answer = self.llm_manager.generate_answer(context, question)

                # fallback if weak answer
                if "not enough information" in answer.lower():
                    answer = f"Closest info:\n{top_chunks[0][:200]}"

            else:
                answer = context[:200]

            return answer, []

        except Exception as e:
            print("❌ QUERY ERROR:", str(e))
            return "Error generating answer", []

    # -------------------------------
    # RECOMMENDATIONS
    # -------------------------------
    def get_recommendations(self, book, n_similar=3):
        try:
            return list(Book.objects.exclude(id=book.id)[:n_similar])
        except:
            return []