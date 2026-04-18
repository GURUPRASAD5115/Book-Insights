# AI-Powered Book Insight Platform - Setup Guide

Complete guide to set up and run the Book Insight Platform locally.

## Project Structure

```
.
├── app/                    # Next.js frontend (Next.js 16.2.0)
├── components/             # React components
├── backend/                # Django REST Framework backend
│   ├── config/             # Django configuration
│   ├── books/              # Books app (models, views, serializers)
│   ├── rag/                # RAG pipeline (embeddings, LLM, vector store)
│   ├── scripts/            # Helper scripts
│   ├── manage.py
│   ├── requirements.txt
│   └── .env.example
└── .env.example            # Frontend env
```

## Prerequisites

- Python 3.9+ (for backend)
- Node.js 18+ (for frontend)
- MySQL (or compatible database)
- OpenAI API key (or local LLM like LM Studio)

## Backend Setup

### 1. Create Virtual Environment

```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure Environment

```bash
cp .env.example .env
# Edit .env with your settings:
# - DB_NAME, DB_USER, DB_PASSWORD
# - OPENAI_API_KEY (if using OpenAI)
# - CORS_ALLOWED_ORIGINS
```

### 4. Run Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### 5. Create Sample Data

```bash
# Option 1: Load sample books (recommended for testing)
python manage.py shell < scripts/sample_data.py

# Option 2: Use Django admin
python manage.py createsuperuser
python manage.py runserver
# Visit http://localhost:8000/admin to add books manually
```

### 6. Process Books (Generate Embeddings)

```bash
# Visit the API endpoint to process books:
# POST http://localhost:8000/api/books/{id}/process/
# This will create chunks and embeddings for the book
```

### 7. Run Backend Server

```bash
python manage.py runserver
```

The backend will be available at `http://localhost:8000`

## Frontend Setup

### 1. Install Dependencies

```bash
npm install
# or
pnpm install
```

### 2. Configure Environment

```bash
cp .env.example .env.local
# Edit .env.local:
# NEXT_PUBLIC_API_URL=http://localhost:8000
```

### 3. Run Frontend Server

```bash
npm run dev
# or
pnpm dev
```

The frontend will be available at `http://localhost:3000`

## API Endpoints

### Books
- `GET /api/books/` - List all books
- `GET /api/books/{id}/` - Get book details
- `POST /api/books/` - Create a new book
- `POST /api/books/{id}/process/` - Process book (generate embeddings)
- `GET /api/books/{id}/insights/` - Get AI insights
- `GET /api/books/{id}/recommendations/` - Get similar books

### RAG Query
- `POST /api/rag/query/` - Ask a question about books

**Example RAG Query:**
```bash
curl -X POST http://localhost:8000/api/rag/query/ \
  -H "Content-Type: application/json" \
  -d '{
    "question": "What are the main themes in the books?"
  }'
```

## Using LM Studio (Local LLM)

Instead of OpenAI, you can use LM Studio for free:

1. Download LM Studio from https://lmstudio.ai/
2. Download a model (e.g., Mistral 7B)
3. Start the local server (default: http://localhost:1234)
4. Modify `backend/rag/llm.py` to use the local endpoint instead of OpenAI

```python
# Change from OpenAI to local LLM
response = requests.post(
    'http://localhost:1234/v1/chat/completions',
    json={
        'model': 'local-model',
        'messages': [...],
        'temperature': 0.7,
    }
)
```

## Database Setup

### MySQL

If using MySQL, ensure you have it running:

```bash
# On macOS with Homebrew
brew services start mysql

# On Linux
sudo systemctl start mysql

# Create database
mysql -u root -p
CREATE DATABASE book_insights;
EXIT;
```

### SQLite (Development)

For development without MySQL:

```python
# In backend/config/settings.py
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
```

## Troubleshooting

### "Connection Refused" Error

- Ensure backend is running: `python manage.py runserver`
- Check `NEXT_PUBLIC_API_URL` in frontend `.env.local`
- Verify CORS settings in Django

### "No such table" Error

- Run migrations: `python manage.py migrate`
- Check database credentials in `.env`

### LLM Not Available

- Ensure `OPENAI_API_KEY` is set or LM Studio is running
- Check backend logs for specific errors
- Fallback to local embeddings without LLM features

### Books Not Showing

- Ensure books are created via admin or sample_data script
- Verify database migrations ran successfully
- Check backend API: `curl http://localhost:8000/api/books/`

## Next Steps

1. **Add More Books**: Use Django admin or create a form to upload books
2. **Customize AI Insights**: Modify `backend/rag/llm.py` for different analysis
3. **Improve Embeddings**: Try different embedding models in `backend/rag/embeddings.py`
4. **Deploy**: Deploy backend to Heroku/Railway and frontend to Vercel
5. **Add Authentication**: Implement user accounts and favorites feature

## Deployment

### Backend (Django)
- Deploy to Heroku, Railway, or Render
- Use managed database (PlanetScale for MySQL)
- Set environment variables in deployment platform

### Frontend (Next.js)
- Deploy to Vercel
- Update `NEXT_PUBLIC_API_URL` to production backend URL
- Set environment variables in deployment settings

## Support

For issues or questions:
1. Check the troubleshooting section above
2. Review backend logs: `python manage.py runserver`
3. Check browser console for frontend errors
4. Test API endpoints directly with curl/Postman

## Resources

- Django REST Framework: https://www.django-rest-framework.org/
- Next.js: https://nextjs.org/
- Sentence Transformers: https://www.sbert.net/
- ChromaDB: https://www.trychroma.com/
- OpenAI API: https://platform.openai.com/docs/
