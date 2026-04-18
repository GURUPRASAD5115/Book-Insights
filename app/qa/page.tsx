'use client';

import { useState, useEffect } from 'react';
import { Header } from '@/components/Header';
import { QAForm } from '@/components/QAForm';
import { AnswerDisplay } from '@/components/AnswerDisplay';
import { Card } from '@/components/ui/card';
import { Loader2 } from 'lucide-react';

interface Book {
  id: number;
  title: string;
  author: string;
  description: string;
  rating: number;
  cover_image?: string;
}

export default function QAPage() {
  const [books, setBooks] = useState<Book[]>([]);
  const [answer, setAnswer] = useState<string | null>(null);
  const [sources, setSources] = useState<number[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [isFetchingBooks, setIsFetchingBooks] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    fetchBooks();
  }, []);

  const fetchBooks = async () => {
    try {
      const apiUrl = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';
      const response = await fetch(`${apiUrl}/api/books/`);
      if (!response.ok) throw new Error('Failed to fetch books');
      const data = await response.json();
      setBooks(data.results || data);
    } catch (err) {
      console.error(err);
    } finally {
      setIsFetchingBooks(false);
    }
  };

  const handleQuery = async (question: string, bookIds?: number[]) => {
    try {
      setIsLoading(true);
      setError(null);
      const apiUrl = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';
      
      const payload = {
        question,
        ...(bookIds && bookIds.length > 0 && { book_ids: bookIds }),
      };

      const response = await fetch(`${apiUrl}/api/rag/query/`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(payload),
      });

      if (!response.ok) throw new Error('Failed to get answer');
      const data = await response.json();
      setAnswer(data.answer);
      setSources(data.sources || []);
    } catch (err) {
      setError('Failed to get an answer. Make sure the backend server is running and has books with embeddings.');
      console.error(err);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <main className="min-h-screen bg-background">
      <Header />

      <section className="py-12 px-4 sm:px-6 lg:px-8">
        <div className="max-w-4xl mx-auto">
          <div className="mb-12">
            <h1 className="text-4xl font-bold text-foreground mb-2">Ask About Books</h1>
            <p className="text-muted-foreground">
              Ask questions about the books in our collection and get intelligent, AI-powered answers with citations.
            </p>
          </div>

          <div className="space-y-8">
            {/* Q&A Form */}
            <Card className="p-8 bg-card border-border">
              <h2 className="text-2xl font-semibold text-foreground mb-6">Ask a Question</h2>
              
              {isFetchingBooks ? (
                <div className="flex items-center gap-2 text-muted-foreground">
                  <Loader2 size={20} className="animate-spin" />
                  <span>Loading books...</span>
                </div>
              ) : books.length === 0 ? (
                <div className="text-muted-foreground">
                  No books available. Please add some books through the admin panel first.
                </div>
              ) : (
                <QAForm onSubmit={handleQuery} isLoading={isLoading} />
              )}

              {error && (
                <div className="mt-4 p-4 bg-red-500/10 border border-red-500/50 text-red-400 rounded-lg text-sm">
                  {error}
                </div>
              )}
            </Card>

            {/* Answer Display */}
            {(answer || isLoading) && (
              <AnswerDisplay
                isLoading={isLoading}
                answer={answer || undefined}
                sources={sources}
                books={books}
              />
            )}

            {/* Tips */}
            {!answer && !isLoading && (
              <Card className="p-8 bg-card/50 border-border">
                <h3 className="text-lg font-semibold text-foreground mb-4">Tips for Better Results</h3>
                <ul className="space-y-2 text-muted-foreground">
                  <li>• Ask specific questions about book content, characters, or themes</li>
                  <li>• The AI will search through all books in our collection for relevant information</li>
                  <li>• Make sure books have been processed to generate embeddings</li>
                  <li>• Use natural language - the AI understands conversational queries</li>
                </ul>
              </Card>
            )}
          </div>
        </div>
      </section>
    </main>
  );
}
