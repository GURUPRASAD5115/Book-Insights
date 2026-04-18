'use client';

import { Card } from '@/components/ui/card';
import { Star } from 'lucide-react';
import Link from 'next/link';

interface Book {
  id: number;
  title: string;
  author: string;
  description: string;
  rating: number;
  cover_image?: string;
}

export function BookCard({ book }: { book: Book }) {
  return (
    <Link href={`/books/${book.id}`}>
      <Card className="h-full cursor-pointer hover:shadow-lg transition-shadow bg-card border-border hover:border-accent">
        <div className="p-6 flex flex-col h-full">
          {book.cover_image && (
            <img
              src={book.cover_image}
              alt={book.title}
              className="w-full h-48 object-cover rounded-lg mb-4"
            />
          )}
          <div className="flex-1">
            <h3 className="font-semibold text-lg text-foreground mb-2 line-clamp-2">
              {book.title}
            </h3>
            <p className="text-sm text-muted-foreground mb-2">{book.author}</p>
            <p className="text-sm text-foreground/80 line-clamp-3 mb-4">
              {book.description}
            </p>
          </div>
          {book.rating > 0 && (
            <div className="flex items-center gap-2 mt-4">
              <div className="flex">
                {[...Array(5)].map((_, i) => (
                  <Star
                    key={i}
                    size={16}
                    className={
                      i < Math.floor(book.rating)
                        ? 'fill-accent text-accent'
                        : 'text-muted-foreground'
                    }
                  />
                ))}
              </div>
              <span className="text-sm text-muted-foreground">{book.rating.toFixed(1)}</span>
            </div>
          )}
        </div>
      </Card>
    </Link>
  );
}
