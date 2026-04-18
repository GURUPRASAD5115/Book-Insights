#!/usr/bin/env python
"""
Script to populate the database with sample book data
Run this after migrations: python manage.py shell < scripts/sample_data.py
"""

import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from books.models import Book

# Sample books data
sample_books = [
    {
        'title': 'To Kill a Mockingbird',
        'author': 'Harper Lee',
        'description': 'A gripping tale of racial injustice and childhood innocence in the American South. Through the eyes of Scout Finch, we witness her father\'s defense of Tom Robinson, a Black man falsely accused of rape. This classic explores themes of morality, prejudice, and the loss of innocence.',
        'rating': 4.8,
        'url': 'https://example.com/books/mockingbird',
        'cover_image': 'https://via.placeholder.com/300x450?text=Mockingbird'
    },
    {
        'title': '1984',
        'author': 'George Orwell',
        'description': 'A dystopian novel set in the totalitarian state of Oceania, where Big Brother watches everyone. Winston Smith attempts to rebel against the oppressive regime, exploring themes of surveillance, totalitarianism, and the power of truth.',
        'rating': 4.6,
        'url': 'https://example.com/books/1984',
        'cover_image': 'https://via.placeholder.com/300x450?text=1984'
    },
    {
        'title': 'Pride and Prejudice',
        'author': 'Jane Austen',
        'description': 'A romantic novel about Elizabeth Bennet, a spirited young woman navigating society and love in Georgian England. Through witty dialogue and sharp social commentary, Austen explores themes of love, class, and personal growth.',
        'rating': 4.7,
        'url': 'https://example.com/books/pride',
        'cover_image': 'https://via.placeholder.com/300x450?text=Pride+and+Prejudice'
    },
    {
        'title': 'The Great Gatsby',
        'author': 'F. Scott Fitzgerald',
        'description': 'Set in the Jazz Age, this novel follows Jay Gatsby and his obsessive pursuit of Daisy Buchanan. Through the eyes of Nick Carraway, Fitzgerald explores themes of wealth, ambition, love, and the American Dream.',
        'rating': 4.5,
        'url': 'https://example.com/books/gatsby',
        'cover_image': 'https://via.placeholder.com/300x450?text=The+Great+Gatsby'
    },
    {
        'title': 'Moby Dick',
        'author': 'Herman Melville',
        'description': 'An epic tale of Captain Ahab\'s obsessive pursuit of the white whale Moby Dick. Through Ishmael\'s narration, Melville explores themes of obsession, fate, and humanity\'s relationship with nature.',
        'rating': 4.2,
        'url': 'https://example.com/books/moby',
        'cover_image': 'https://via.placeholder.com/300x450?text=Moby+Dick'
    },
    {
        'title': 'Jane Eyre',
        'author': 'Charlotte Brontë',
        'description': 'The story of Jane Eyre, an orphan girl who becomes a governess and falls in love with the mysterious Mr. Rochester. This Gothic romance explores themes of independence, morality, and true love.',
        'rating': 4.6,
        'url': 'https://example.com/books/jane-eyre',
        'cover_image': 'https://via.placeholder.com/300x450?text=Jane+Eyre'
    },
]

# Create books
created_count = 0
for book_data in sample_books:
    book, created = Book.objects.get_or_create(
        title=book_data['title'],
        author=book_data['author'],
        defaults={
            'description': book_data['description'],
            'rating': book_data['rating'],
            'url': book_data['url'],
            'cover_image': book_data['cover_image'],
        }
    )
    if created:
        created_count += 1
        print(f"Created: {book.title} by {book.author}")
    else:
        print(f"Already exists: {book.title} by {book.author}")

print(f"\nTotal new books created: {created_count}")
