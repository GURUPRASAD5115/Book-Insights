'use client';

import { useState, useEffect } from 'react';
import { Header } from '@/components/Header';
import { BookCard } from '@/components/BookCard';
import { SearchBar } from '@/components/SearchBar';
import { Loader2 } from 'lucide-react';
import { Empty } from '@/components/ui/empty';

interface Book {
  id: number;
  title: string;
  author: string;
  description: string;
  rating: number;
  cover_image?: string;
}

// ✅ Django paginated response type
interface ApiResponse {
  count?: number;
  next?: string | null;
  previous?: string | null;
  results?: Book[];
}

export default function BooksPage() {
  const [books, setBooks] = useState<Book[]>([]);
  const [searchQuery, setSearchQuery] = useState('');
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    fetchBooks();
  }, []);

  const fetchBooks = async () => {
    try {
      setIsLoading(true);
      setError(null);

      const response = await fetch('http://127.0.0.1:8000/api/books/', {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
        },
      });

      // ✅ Better error handling
      if (!response.ok) {
        throw new Error(`HTTP error: ${response.status}`);
      }

      const data: ApiResponse = await response.json();

      // ✅ Safe data handling
      if (data.results) {
        setBooks(data.results);
      } else if (Array.isArray(data)) {
        setBooks(data);
      } else {
        setBooks([]);
      }
    } catch (err: any) {
      console.error('Fetch error:', err);
      setError('Failed to load books. Check backend server.');
    } finally {
      setIsLoading(false);
    }
  };

  const filteredBooks = books.filter(
    (book) =>
      book.title.toLowerCase().includes(searchQuery.toLowerCase()) ||
      book.author.toLowerCase().includes(searchQuery.toLowerCase()) ||
      book.description.toLowerCase().includes(searchQuery.toLowerCase())
  );

  return (
    <main className="min-h-screen bg-background">
      <Header />

      <section className="py-12 px-4 sm:px-6 lg:px-8">
        <div className="max-w-7xl mx-auto">

          {/* Heading */}
          <div className="mb-8">
            <h1 className="text-4xl font-bold text-foreground mb-2">
              Browse Books
            </h1>
            <p className="text-muted-foreground">
              Discover your collection
            </p>
          </div>

          {/* Search */}
          <div className="mb-8 max-w-md">
            <SearchBar
              value={searchQuery}
              onChange={setSearchQuery}
              placeholder="Search by title, author..."
            />
          </div>

          {/* Error */}
          {error && (
            <div className="bg-red-500/10 border border-red-500/50 text-red-400 px-4 py-3 rounded-lg mb-8">
              {error}
            </div>
          )}

          {/* Loading */}
          {isLoading ? (
            <div className="flex justify-center items-center py-12">
              <Loader2 className="w-8 h-8 animate-spin" />
            </div>
          ) : filteredBooks.length === 0 ? (
            <Empty description="No books found." />
          ) : (
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
              {filteredBooks.map((book) => (
                <BookCard key={book.id} book={book} />
              ))}
            </div>
          )}

        </div>
      </section>
    </main>
  );
}