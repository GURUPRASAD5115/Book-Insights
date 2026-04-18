import chromadb
from chromadb.config import Settings
import os
import logging

logger = logging.getLogger(__name__)


class VectorStore:
    def __init__(self, path='chroma_data'):
        """Initialize ChromaDB vector store"""
        try:
            os.makedirs(path, exist_ok=True)
            settings = Settings(
                chroma_db_impl='duckdb+parquet',
                persist_directory=path,
                anonymized_telemetry=False,
            )
            self.client = chromadb.Client(settings)
            self.collection = self.client.get_or_create_collection(
                name='books',
                metadata={'hnsw:space': 'cosine'}
            )
            logger.info("ChromaDB initialized successfully")
        except Exception as e:
            logger.error(f"Error initializing ChromaDB: {str(e)}")
            raise

    def add_documents(self, documents, embeddings, metadatas, ids):
        """Add documents with embeddings to the vector store"""
        try:
            self.collection.add(
                documents=documents,
                embeddings=embeddings,
                metadatas=metadatas,
                ids=ids
            )
            logger.info(f"Added {len(documents)} documents to vector store")
        except Exception as e:
            logger.error(f"Error adding documents: {str(e)}")
            raise

    def query(self, query_embedding, n_results=5):
        """Query the vector store for similar documents"""
        try:
            results = self.collection.query(
                query_embeddings=[query_embedding],
                n_results=n_results
            )
            return results
        except Exception as e:
            logger.error(f"Error querying vector store: {str(e)}")
            raise

    def delete_by_book(self, book_id):
        """Delete all chunks for a specific book"""
        try:
            self.collection.delete(
                where={'book_id': {'$eq': book_id}}
            )
            logger.info(f"Deleted all chunks for book {book_id}")
        except Exception as e:
            logger.error(f"Error deleting documents: {str(e)}")
            raise

    def persist(self):
        """Persist the vector store to disk"""
        try:
            self.client.persist()
            logger.info("Vector store persisted")
        except Exception as e:
            logger.error(f"Error persisting vector store: {str(e)}")
