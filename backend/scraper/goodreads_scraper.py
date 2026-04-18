"""
Web scraper for collecting book data from online sources
This is a basic example that can be extended
"""

import os
import sys
import django
import requests
from bs4 import BeautifulSoup

# Setup Django
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from books.models import Book


class BookScraper:
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        self.timeout = 10

    def scrape_project_gutenberg_books(self, num_books=10):
        """
        Scrape popular books from Project Gutenberg
        Note: This is a simplified example. In production, consider using their API.
        """
        print(f"Attempting to scrape {num_books} books from Project Gutenberg...")
        
        # In practice, you would make requests to Project Gutenberg API or website
        # For now, we'll skip actual scraping to avoid making external requests
        print("Scraping disabled to avoid external requests.")
        print("Use the sample_data.py script to load sample books instead.")

    def add_book_from_data(self, title, author, description, rating=0, url='', cover_image=''):
        """
        Add a book to the database from scraped data
        """
        try:
            book, created = Book.objects.get_or_create(
                title=title,
                author=author,
                defaults={
                    'description': description,
                    'rating': rating,
                    'url': url,
                    'cover_image': cover_image,
                }
            )
            
            if created:
                print(f"✓ Added: {title} by {author}")
                return book
            else:
                print(f"- Exists: {title} by {author}")
                return book
                
        except Exception as e:
            print(f"✗ Error adding {title}: {str(e)}")
            return None

    def process_newly_added_books(self):
        """
        Process all unprocessed books to generate embeddings
        """
        from rag.pipeline import RAGPipeline
        
        unprocessed_books = Book.objects.filter(processed=False)
        pipeline = RAGPipeline()
        
        for book in unprocessed_books:
            try:
                print(f"Processing: {book.title}...")
                pipeline.process_book(book)
                book.processed = True
                book.save()
                print(f"✓ Processed: {book.title}")
            except Exception as e:
                print(f"✗ Error processing {book.title}: {str(e)}")

    def generate_insights(self):
        """
        Generate AI insights for all books
        """
        from rag.pipeline import RAGPipeline
        
        books_without_insights = Book.objects.filter(insight__isnull=True)
        pipeline = RAGPipeline()
        
        for book in books_without_insights:
            try:
                print(f"Generating insights for: {book.title}...")
                pipeline.generate_insights(book)
                print(f"✓ Generated insights for: {book.title}")
            except Exception as e:
                print(f"✗ Error generating insights for {book.title}: {str(e)}")


def main():
    scraper = BookScraper()
    
    print("=" * 60)
    print("Book Data Scraper & Processor")
    print("=" * 60)
    print()
    
    # Note: We're not doing actual web scraping to avoid external dependencies
    # Instead, use sample_data.py to load initial data
    print("To load sample data, run: python manage.py shell < scripts/sample_data.py")
    print()
    
    # Process books to generate embeddings
    print("Processing books to generate embeddings...")
    scraper.process_newly_added_books()
    print()
    
    # Generate AI insights
    print("Generating AI insights for books...")
    scraper.generate_insights()
    print()
    
    print("✓ Done! Your book database is ready.")
    print("Visit http://localhost:8000 to view the books.")


if __name__ == '__main__':
    main()
