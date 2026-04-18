'use client';

import { Card } from '@/components/ui/card';
import { Loader2 } from 'lucide-react';

interface AnswerDisplayProps {
  isLoading: boolean;
  answer?: string;
  sources?: number[];
  books?: any[];
}

export function AnswerDisplay({ isLoading, answer, sources = [], books = [] }: AnswerDisplayProps) {
  if (isLoading) {
    return (
      <Card className="p-6 bg-card border-border">
        <div className="flex items-center gap-2 text-muted-foreground">
          <Loader2 size={20} className="animate-spin" />
          <span>Thinking...</span>
        </div>
      </Card>
    );
  }

  if (!answer) {
    return null;
  }

  return (
    <Card className="p-6 bg-card border-border">
      <h3 className="text-lg font-semibold text-foreground mb-4">Answer</h3>
      <p className="text-foreground/90 mb-6 whitespace-pre-wrap">{answer}</p>

      {sources && sources.length > 0 && (
        <div>
          <h4 className="text-sm font-semibold text-muted-foreground mb-3">Sources</h4>
          <div className="space-y-2">
            {sources.map((bookId) => {
              const book = books.find((b) => b.id === bookId);
              return (
                <div key={bookId} className="text-sm text-muted-foreground">
                  {book ? (
                    <>
                      <span className="font-medium text-foreground">{book.title}</span> by {book.author}
                    </>
                  ) : (
                    `Book ID: ${bookId}`
                  )}
                </div>
              );
            })}
          </div>
        </div>
      )}
    </Card>
  );
}
