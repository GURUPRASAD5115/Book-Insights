'use client';

import { useState } from 'react';

export default function AddBook() {
  const [form, setForm] = useState({
    title: '',
    author: '',
    description: '',
    rating: '',
    url: '',
    cover_image: ''
  });

  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState('');

  // Handle input change
  const handleChange = (e) => {
    const { name, value } = e.target;

    setForm((prev) => ({
      ...prev,
      [name]: value ?? '' // never undefined
    }));
  };

  // Handle form submit
  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setMessage('');

    try {
      const response = await fetch('http://127.0.0.1:8000/api/books/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          ...form,
          rating: form.rating ? parseFloat(form.rating) : 0
        })
      });

      if (!response.ok) {
        throw new Error('Failed to add book');
      }

      const data = await response.json();
      const bookId = data.id;

      // Optional backend processing
      await fetch(`http://127.0.0.1:8000/api/books/${bookId}/process/`, {
        method: 'POST'
      });

      setMessage('✅ Book added & processed successfully!');

      // Reset form (IMPORTANT: include ALL fields)
      setForm({
        title: '',
        author: '',
        description: '',
        rating: '',
        url: '',
        cover_image: ''
      });

    } catch (error) {
      console.error(error);
      setMessage('❌ Error adding book. Check backend.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-black to-blue-900 p-4">

      <div className="bg-white/10 backdrop-blur-lg p-8 rounded-2xl shadow-xl w-full max-w-lg text-white">

        <h1 className="text-2xl font-bold mb-6 text-center">
          📚 Add New Book
        </h1>

        <form onSubmit={handleSubmit} className="space-y-4">

          {/* Title */}
          <input
            type="text"
            name="title"
            placeholder="Book Title *"
            value={form.title}
            onChange={handleChange}
            required
            className="w-full p-3 rounded-lg bg-white/20 outline-none"
          />

          {/* Author */}
          <input
            type="text"
            name="author"
            placeholder="Author Name *"
            value={form.author}
            onChange={handleChange}
            required
            className="w-full p-3 rounded-lg bg-white/20 outline-none"
          />

          {/* Description */}
          <textarea
            name="description"
            placeholder="Book Description *"
            value={form.description}
            onChange={handleChange}
            required
            rows={4}
            className="w-full p-3 rounded-lg bg-white/20 outline-none"
          />

          {/* Rating */}
          <input
            type="number"
            name="rating"
            placeholder="Rating (0–5)"
            value={form.rating}
            onChange={handleChange}
            min="0"
            max="5"
            step="0.1"
            className="w-full p-3 rounded-lg bg-white/20 outline-none"
          />

          {/* Book URL */}
          <input
            type="url"
            name="url"
            placeholder="Book URL (optional)"
            value={form.url}
            onChange={handleChange}
            className="w-full p-3 rounded-lg bg-white/20 outline-none"
          />

          {/* Cover Image URL */}
          <input
            type="url"
            name="cover_image"
            placeholder="Cover Image URL (optional)"
            value={form.cover_image}
            onChange={handleChange}
            className="w-full p-3 rounded-lg bg-white/20 outline-none"
          />

          {/* Image Preview */}
          {form.cover_image && (
            <img
              src={form.cover_image}
              alt="Cover Preview"
              className="w-full h-48 object-cover rounded-lg border border-white/20"
              onError={(e) => (e.currentTarget.style.display = 'none')}
            />
          )}

          {/* Submit Button */}
          <button
            type="submit"
            disabled={loading}
            className="w-full bg-blue-500 hover:bg-blue-600 transition p-3 rounded-lg font-semibold"
          >
            {loading ? 'Adding...' : 'Add Book 🚀'}
          </button>

        </form>

        {/* Message */}
        {message && (
          <p className="mt-4 text-center text-sm">{message}</p>
        )}

      </div>
    </div>
  );
}