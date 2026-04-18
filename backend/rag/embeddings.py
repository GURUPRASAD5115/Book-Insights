import numpy as np
import logging

logger = logging.getLogger(__name__)

from sentence_transformers import SentenceTransformer


class EmbeddingManager:
    def __init__(self, model_name='all-MiniLM-L6-v2'):
        """Initialize embedding model (STRICT + SAFE)"""
        try:
            print("🚀 Loading embedding model...")

            self.model = SentenceTransformer(model_name)

            print("✅ Embedding model loaded successfully")

        except Exception as e:
            print("❌ MODEL LOAD ERROR:", str(e))
            logger.error(f"Embedding model load failed: {str(e)}")
            self.model = None

    # -----------------------------
    # SINGLE TEXT EMBEDDING
    # -----------------------------
    def embed_text(self, text):
        try:
            if not text:
                return [0.0] * 384  # safe fallback

            if not self.model:
                raise ValueError("Model not loaded")

            embedding = self.model.encode(text)

            # ensure list format
            if hasattr(embedding, "tolist"):
                return embedding.tolist()

            return list(embedding)

        except Exception as e:
            print("❌ Embedding error:", str(e))
            logger.error(f"Embedding error: {str(e)}")

            # 🔥 CRITICAL: never return None
            return [0.0] * 384

    # -----------------------------
    # MULTIPLE TEXT EMBEDDINGS
    # -----------------------------
    def embed_texts(self, texts):
        try:
            if not texts:
                return []

            if not self.model:
                raise ValueError("Model not loaded")

            embeddings = self.model.encode(texts)

            return [
                emb.tolist() if hasattr(emb, "tolist") else list(emb)
                for emb in embeddings
            ]

        except Exception as e:
            print("❌ Batch embedding error:", str(e))
            logger.error(f"Batch embedding error: {str(e)}")

            return [[0.0] * 384 for _ in texts]

    # -----------------------------
    # COSINE SIMILARITY
    # -----------------------------
    def similarity(self, embedding1, embedding2):
        try:
            if not embedding1 or not embedding2:
                return 0.0

            e1 = np.array(embedding1)
            e2 = np.array(embedding2)

            # ensure same shape
            if e1.shape != e2.shape:
                logger.warning(f"Shape mismatch: {e1.shape} vs {e2.shape}")
                return 0.0

            norm1 = np.linalg.norm(e1)
            norm2 = np.linalg.norm(e2)

            if norm1 == 0 or norm2 == 0:
                return 0.0

            similarity = np.dot(e1, e2) / (norm1 * norm2)

            return float(similarity)

        except Exception as e:
            print("❌ Similarity error:", str(e))
            logger.error(f"Similarity error: {str(e)}")
            return 0.0