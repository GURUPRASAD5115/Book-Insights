'use client';

import { useState, useEffect } from 'react';
import { Header } from '@/components/Header';
import { Button } from '@/components/ui/button';
import { Card } from '@/components/ui/card';
import { Loader2, ArrowLeft, Star } from 'lucide-react';
import Link from 'next/link';
import { useParams } from 'next/navigation';

interface Book {
  id: number;
  title: string;
  author: string;
  description: string;
  rating: number;
  cover_image?: string;
  processed?: boolean;
}

interface Insight {
  id: number;
  summary?: string;
  genres?: string[];
  sentiment?: string;
  recommendations?: number[];
}

export default function BookDetailPage() {
  const params = useParams();
  const bookId = params.id as string;
  
  const [book, setBook] = useState<Book | null>(null);
  const [insight, setInsight] = useState<Insight | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [isProcessing, setIsProcessing] = useState(false);

  useEffect(() => {
    fetchBook();
  }, [bookId]);

  const fetchBook = async () => {
    try {
      setIsLoading(true);
      const apiUrl = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';
      const response = await fetch(`${apiUrl}/api/books/${bookId}/`);
      if (!response.ok) throw new Error('Failed to fetch book');
      const data = await response.json();
      setBook(data);
      if (data.insight) {
        setInsight(data.insight);
      }
      setError(null);
    } catch (err) {
      setError('Failed to load book details');
      console.error(err);
    } finally {
      setIsLoading(false);
    }
  };

  const processBook = async () => {
    try {
      setIsProcessing(true);
      const apiUrl = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';
      const response = await fetch(`${apiUrl}/api/books/${bookId}/process/`, {
        method: 'POST',
      });
      if (!response.ok) throw new Error('Failed to process book');
      await fetchBook();
    } catch (err) {
      setError('Failed to process book');
      console.error(err);
    } finally {
      setIsProcessing(false);
    }
  };

  if (isLoading) {
    return (
      <main className="min-h-screen bg-background">
        <Header />
        <div className="flex justify-center items-center py-32">
          <Loader2 className="w-8 h-8 text-accent animate-spin" />
        </div>
      </main>
    );
  }

  if (error || !book) {
    return (
      <main className="min-h-screen bg-background">
        <Header />
        <div className="max-w-7xl mx-auto px-4 py-8">
          <Link href="/books">
            <Button variant="outline" className="mb-6 gap-2">
              <ArrowLeft size={20} /> Back to Books
            </Button>
          </Link>
          <div className="text-center text-red-400">{error || 'Book not found'}</div>
        </div>
      </main>
    );
  }

  return (
    <main className="min-h-screen bg-background">
      <Header />

      <section className="py-12 px-4 sm:px-6 lg:px-8">
        <div className="max-w-4xl mx-auto">
          <Link href="/books">
            <Button variant="outline" className="mb-6 gap-2">
              <ArrowLeft size={20} /> Back to Books
            </Button>
          </Link>

          <div className="grid md:grid-cols-3 gap-8">
            {/* Book Info */}
            <div className="md:col-span-2 space-y-6">
              <div>
                <h1 className="text-4xl font-bold text-foreground mb-2">{book.title}</h1>
                <p className="text-xl text-muted-foreground mb-4">{book.author}</p>
                
                {book.rating > 0 && (
                  <div className="flex items-center gap-2 mb-4">
                    <div className="flex">
                      {[...Array(5)].map((_, i) => (
                        <Star
                          key={i}
                          size={20}
                          className={
                            i < Math.floor(book.rating)
                              ? 'fill-accent text-accent'
                              : 'text-muted-foreground'
                          }
                        />
                      ))}
                    </div>
                    <span className="text-muted-foreground">{book.rating.toFixed(1)}</span>
                  </div>
                )}

                <p className="text-foreground/90 leading-relaxed">{book.description}</p>
              </div>

              {/* Insights */}
              {insight && (
                <div className="space-y-4">
                  {insight.summary && (
                    <Card className="p-6 bg-card border-border">
                      <h3 className="text-lg font-semibold text-foreground mb-3">Summary</h3>
                      <p className="text-foreground/90">{insight.summary}</p>
                    </Card>
                  )}

                  {insight.genres && insight.genres.length > 0 && (
                    <Card className="p-6 bg-card border-border">
                      <h3 className="text-lg font-semibold text-foreground mb-3">Genres</h3>
                      <div className="flex flex-wrap gap-2">
                        {insight.genres.map((genre) => (
                          <span
                            key={genre}
                            className="px-3 py-1 bg-accent/20 text-accent rounded-full text-sm"
                          >
                            {genre}
                          </span>
                        ))}
                      </div>
                    </Card>
                  )}

                  {insight.sentiment && (
                    <Card className="p-6 bg-card border-border">
                      <h3 className="text-lg font-semibold text-foreground mb-3">Sentiment</h3>
                      <p className="text-foreground/90 capitalize">{insight.sentiment}</p>
                    </Card>
                  )}
                </div>
              )}

              {!insight && (
                <Card className="p-6 bg-card border-border">
                  <p className="text-muted-foreground mb-4">
                    AI insights not yet generated for this book. Click the button below to generate them.
                  </p>
                  <Button
                    onClick={processBook}
                    disabled={isProcessing}
                    className="bg-accent hover:bg-accent/90 text-accent-foreground gap-2"
                  >
                    {isProcessing && <Loader2 size={20} className="animate-spin" />}
                    Generate Insights
                  </Button>
                </Card>
              )}
            </div>

            {/* Sidebar */}
            <div className="space-y-4">
              {book.cover_image && (
                <img
                  src={book.cover_image}
                  alt={book.title}
                  className="w-full rounded-lg shadow-lg"
                />
              )}
              
              <Card className="p-4 bg-card border-border">
                <h4 className="font-semibold text-foreground mb-2">About this Book</h4>
                <dl className="space-y-3 text-sm">
                  <div>
                    <dt className="text-muted-foreground">Author</dt>
                    <dd className="text-foreground">{book.author}</dd>
                  </div>
                  <div>
                    <dt className="text-muted-foreground">Status</dt>
                    <dd className="text-foreground">
                      {book.processed ? '✓ Processed' : 'Not processed'}
                    </dd>
                  </div>
                </dl>
              </Card>

              <Link href="/qa" className="block">
                <Button className="w-full bg-accent hover:bg-accent/90 text-accent-foreground">
                  Ask about this book
                </Button>
              </Link>
            </div>
          </div>
        </div>
      </section>
    </main>
  );
}
