# Book Insight Backend

Django REST Framework backend for the AI-Powered Book Insight Platform.

## Setup

1. Create virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Create `.env` file:
   ```bash
   cp .env.example .env
   # Edit .env with your settings
   ```

4. Run migrations:
   ```bash
   python manage.py migrate
   ```

5. Create superuser:
   ```bash
   python manage.py createsuperuser
   ```

6. Run development server:
   ```bash
   python manage.py runserver
   ```

## API Endpoints

### Books
- `GET /api/books/` - List all books
- `GET /api/books/{id}/` - Get book details
- `POST /api/books/` - Create a book
- `POST /api/books/{id}/process/` - Process book (generate embeddings)
- `GET /api/books/{id}/insights/` - Get book insights
- `GET /api/books/{id}/recommendations/` - Get similar books

### RAG Query
- `POST /api/rag/query/` - Ask a question about books

## Environment Variables

See `.env.example` for all required environment variables.

## Models

- **Book**: Store book metadata (title, author, description, etc.)
- **BookChunk**: Store text chunks with embeddings
- **BookInsight**: Store generated summaries, genres, sentiment analysis
- **UserQuery**: Store user questions and AI-generated answers
- **ChatHistory**: Store chat conversation history
