'use client';

import { useState } from 'react';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Send, Loader2 } from 'lucide-react';

interface QAFormProps {
  onSubmit: (question: string, bookIds?: number[]) => Promise<void>;
  isLoading?: boolean;
  selectedBookIds?: number[];
}

export function QAForm({ onSubmit, isLoading = false, selectedBookIds }: QAFormProps) {
  const [question, setQuestion] = useState('');

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (question.trim()) {
      await onSubmit(question, selectedBookIds);
      setQuestion('');
    }
  };

  return (
    <form onSubmit={handleSubmit} className="w-full">
      <div className="flex gap-2">
        <Input
          placeholder="Ask a question about the books..."
          value={question}
          onChange={(e) => setQuestion(e.target.value)}
          disabled={isLoading}
          className="flex-1 bg-input border-border text-foreground placeholder:text-muted-foreground"
        />
        <Button
          type="submit"
          disabled={isLoading || !question.trim()}
          className="bg-accent hover:bg-accent/90 text-accent-foreground"
        >
          {isLoading ? <Loader2 size={20} className="animate-spin" /> : <Send size={20} />}
        </Button>
      </div>
    </form>
  );
}
