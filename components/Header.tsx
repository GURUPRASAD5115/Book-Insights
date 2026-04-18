'use client';

import Link from 'next/link';
import { BookOpen } from 'lucide-react';

export function Header() {
  return (
    <header className="border-b border-border bg-card/50 backdrop-blur-sm sticky top-0 z-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
        <nav className="flex items-center justify-between">
          <Link href="/" className="flex items-center gap-2 hover:opacity-80 transition-opacity">
            <BookOpen className="w-8 h-8 text-accent" />
            <span className="text-xl font-bold text-foreground">Book Insights</span>
          </Link>
          <div className="flex items-center gap-6">
            <Link href="/books" className="text-foreground hover:text-accent transition-colors">
              Browse Books
            </Link>
            <Link href="/qa" className="text-foreground hover:text-accent transition-colors">
              Q&A
            </Link>
          </div>
        </nav>
      </div>
    </header>
  );
}
