'use client';

import { Header } from '@/components/Header';
import { Button } from '@/components/ui/button';
import { ArrowRight, BookOpen, Sparkles, MessageCircle } from 'lucide-react';
import Link from 'next/link';

export default function Home() {
  return (
    <main className="min-h-screen bg-background">

      <Header />

      
      {/* Hero Section */}
      <section className="relative py-20 px-4 sm:px-6 lg:px-8">
        <div className="max-w-7xl mx-auto">
          <div className="text-center space-y-8">
            <div className="space-y-4">
              <h1 className="text-5xl sm:text-6xl font-bold text-foreground text-balance">
                Discover Books with <span className="text-accent">AI Insights</span>
              </h1>
              <p className="text-xl text-muted-foreground max-w-2xl mx-auto text-balance">
                Explore a curated collection of books with intelligent AI-powered summaries, genre classification, and instant answers to your questions.
              </p>
            </div>

            <div className="flex flex-col sm:flex-row gap-4 justify-center pt-8">
              <Link href="/books">
                <Button size="lg" className="bg-accent hover:bg-accent/90 text-accent-foreground gap-2">
                  Start Exploring <ArrowRight size={20} />
                </Button>
              </Link>
              <Link href="/qa">
                <Button size="lg" variant="outline" className="border-border text-foreground hover:bg-card gap-2">
                  Ask a Question <MessageCircle size={20} />
                </Button>
              </Link>
            </div>

<div style={{ padding: '10px' }}>
  <Link href="/add-book">
    <button style={{
      background: 'green',
      color: 'white',
      padding: '10px',
      borderRadius: '5px'
    }}>
      + Add Book
    </button>
  </Link>
</div>




          </div>
        </div>
      </section>

      {/* Features Section */}
      <section className="py-20 px-4 sm:px-6 lg:px-8 bg-card/50">
        <div className="max-w-7xl mx-auto">
          <h2 className="text-3xl font-bold text-foreground text-center mb-16">Powerful Features</h2>
          
          <div className="grid md:grid-cols-3 gap-8">
            {/* Feature 1 */}
            <div className="bg-card border border-border rounded-lg p-8 hover:border-accent transition-colors">
              <Sparkles className="w-12 h-12 text-accent mb-4" />
              <h3 className="text-xl font-semibold text-foreground mb-3">AI Summaries</h3>
              <p className="text-muted-foreground">
                Get intelligent summaries of books powered by advanced AI models, capturing the essence of each story.
              </p>
            </div>

            {/* Feature 2 */}
            <div className="bg-card border border-border rounded-lg p-8 hover:border-accent transition-colors">
              <BookOpen className="w-12 h-12 text-accent mb-4" />
              <h3 className="text-xl font-semibold text-foreground mb-3">Genre Classification</h3>
              <p className="text-muted-foreground">
                Automatically categorize books into genres, making it easy to discover your next favorite read.
              </p>
            </div>

            {/* Feature 3 */}
            <div className="bg-card border border-border rounded-lg p-8 hover:border-accent transition-colors">
              <MessageCircle className="w-12 h-12 text-accent mb-4" />
              <h3 className="text-xl font-semibold text-foreground mb-3">Smart Q&A</h3>
              <p className="text-muted-foreground">
                Ask questions about books and get intelligent, contextual answers with proper citations.
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="py-20 px-4 sm:px-6 lg:px-8">
        <div className="max-w-3xl mx-auto text-center space-y-8">
          <h2 className="text-4xl font-bold text-foreground">Ready to Explore?</h2>
          <p className="text-lg text-muted-foreground">
            Browse our collection of books or ask questions about their content with our AI-powered assistant.
          </p>
          <Link href="/books">
            <Button size="lg" className="bg-accent hover:bg-accent/90 text-accent-foreground">
              View All Books
            </Button>
          </Link>
        </div>
      </section>
    </main>
  );
}
