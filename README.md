# AI-Powered Book Insight Platform

A full-stack web application that uses AI and Retrieval-Augmented Generation (RAG) to provide intelligent insights about books and answer questions about their content.

## Features

- **AI-Powered Book Discovery**: Browse a curated collection of books with intelligent categorization
- **Automatic Summaries**: Get AI-generated summaries of books using advanced language models
- **Genre Classification**: Automatically categorize books into relevant genres
- **Sentiment Analysis**: Analyze the tone and sentiment of book descriptions
- **Smart Q&A**: Ask questions about books and get intelligent, contextual answers with proper citations
- **Vector Embeddings**: Fast similarity search using sentence embeddings
- **Responsive Design**: Beautiful, modern UI that works on all devices

## Tech Stack

### Backend
- **Framework**: Django REST Framework
- **Database**: MySQL (configurable)
- **AI/ML**:
  - Sentence Transformers (embeddings)
  - ChromaDB (vector store)
  - OpenAI API or LM Studio (LLM)
- **Languages**: Python 3.9+

### Frontend
- **Framework**: Next.js 16.2.0 with React 19
- **Styling**: Tailwind CSS with custom dark theme
- **Components**: shadcn/ui
- **Language**: TypeScript

### Architecture
```
┌─────────────────────────────────────────────────────────────┐
│                    User Interface (Next.js)                  │
│                  - Homepage & Book Discovery                 │
│                  - Book Details & Insights                   │
│                  - Q&A Interface                             │
└────────────────────────────┬────────────────────────────────┘
                             │
                    API Calls (REST)
                             │
┌────────────────────────────▼────────────────────────────────┐
│               Backend (Django REST Framework)                │
│  ┌──────────────────────────────────────────────────────┐   │
│  │  API Endpoints:                                      │   │
│  │  - GET  /api/books/        → List all books         │   │
│  │  - GET  /api/books/{id}/   → Book details           │   │
│  │  - POST /api/books/        → Create book            │   │
│  │  - POST /api/books/{id}/process/  → Generate emb.   │   │
│  │  - GET  /api/books/{id}/insights/ → AI insights     │   │
│  │  - POST /api/rag/query/    → Ask questions          │   │
│  └──────────────────────────────────────────────────────┘   │
│  ┌──────────────────────────────────────────────────────┐   │
│  │  RAG Pipeline:                                       │   │
│  │  1. Document Chunking  → Text chunks                │   │
│  │  2. Embeddings         → Vector embeddings           │   │
│  │  3. Vector Store       → ChromaDB                    │   │
│  │  4. Similarity Search  → Find relevant chunks        │   │
│  │  5. LLM Integration    → Generate answers            │   │
│  └──────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
                             │
┌────────────────────────────▼────────────────────────────────┐
│               Data Layer                                     │
│  ┌──────────────────────────────────────────────────────┐   │
│  │  MySQL Database                                     │   │
│  │  - Books table                                      │   │
│  │  - BookChunks table (for embeddings)               │   │
│  │  - BookInsights table (summaries, genres)          │   │
│  │  - ChatHistory table (queries & answers)           │   │
│  └──────────────────────────────────────────────────────┘   │
│  ┌──────────────────────────────────────────────────────┐   │
│  │  ChromaDB Vector Store                             │   │
│  │  - Persistent vector embeddings                     │   │
│  │  - Fast similarity search                           │   │
│  └──────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
```

## Project Structure

```
.
├── app/                                # Next.js frontend
│   ├── page.tsx                       # Homepage
│   ├── books/
│   │   ├── page.tsx                   # Books listing
│   │   └── [id]/
│   │       └── page.tsx               # Book details
│   ├── qa/
│   │   └── page.tsx                   # Q&A interface
│   ├── layout.tsx                     # Root layout
│   └── globals.css                    # Global styles
│
├── components/                         # React components
│   ├── Header.tsx                     # Navigation header
│   ├── BookCard.tsx                   # Book card component
│   ├── SearchBar.tsx                  # Search input
│   ├── QAForm.tsx                     # Question input form
│   ├── AnswerDisplay.tsx              # Answer display
│   └── ui/                            # shadcn/ui components
│
├── backend/                           # Django REST Framework
│   ├── config/
│   │   ├── settings.py               # Django settings
│   │   ├── urls.py                   # URL routing
│   │   └── wsgi.py                   # WSGI config
│   │
│   ├── books/                        # Books app
│   │   ├── models.py                 # Database models
│   │   ├── serializers.py            # API serializers
│   │   ├── views.py                  # API views
│   │   ├── urls.py                   # App URLs
│   │   └── admin.py                  # Admin interface
│   │
│   ├── rag/                          # RAG pipeline
│   │   ├── embeddings.py             # Embedding manager
│   │   ├── vector_store.py           # ChromaDB wrapper
│   │   ├── llm.py                    # LLM integration
│   │   └── pipeline.py               # RAG pipeline logic
│   │
│   ├── scraper/                      # Data collection
│   │   └── goodreads_scraper.py      # Web scraper
│   │
│   ├── scripts/                      # Helper scripts
│   │   ├── sample_data.py            # Load sample data
│   │   └── setup_db.sh               # DB setup
│   │
│   ├── manage.py                     # Django CLI
│   ├── requirements.txt              # Python dependencies
│   ├── .env.example                  # Environment template
│   └── README.md                     # Backend docs
│
├── SETUP.md                          # Complete setup guide
└── README.md                         # This file
```

## Screen Shots 
<img width="1920" height="1020" alt="Screenshot 2026-04-18 172459" src="https://github.com/user-attachments/assets/9e1ec095-bce3-417a-8cbf-fbeb96ee3efd" />
<img width="1920" height="1020" alt="Screenshot 2026-04-18 173423" src="https://github.com/user-attachments/assets/b7b00060-3343-4c51-b3a0-c1e3e5651a58" />
<img width="1920" height="1020" alt="Screenshot 2026-04-18 180252" src="https://github.com/user-attachments/assets/6ac47c0e-b555-4a08-996c-aa7594668147" />
<img width="1920" height="1020" alt="Screenshot 2026-04-18 180213" src="https://github.com/user-attachments/assets/33ef7894-c89f-415a-bfd6-3db9fe578382" />
<img width="1920" height="1020" alt="Screenshot 2026-04-18 173753" src="https://github.com/user-attachments/assets/512e1be9-acbe-4c50-a634-764b34639800" />

## Quick Start

### Prerequisites
- Python 3.9+
- Node.js 18+
- MySQL 8.0+

### Backend Setup (5 minutes)

```bash
# 1. Navigate to backend directory
cd backend

# 2. Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Setup environment
cp .env.example .env
# Edit .env with your settings (database credentials, API keys)

# 5. Run migrations
python manage.py makemigrations
python manage.py migrate

# 6. Load sample data
python manage.py shell < scripts/sample_data.py

# 7. Start development server
python manage.py runserver
```

Backend will be available at `http://localhost:8000`

### Frontend Setup (5 minutes)

```bash
# 1. Install dependencies
npm install

# 2. Setup environment
cp .env.example .env.local
# Edit .env.local: NEXT_PUBLIC_API_URL=http://localhost:8000

# 3. Start development server
npm run dev
```

Frontend will be available at `http://localhost:3000`

## Usage

### 1. Add Books
Visit `http://localhost:8000/admin` and add books manually, or run:
```bash
python manage.py shell < backend/scripts/sample_data.py
```

### 2. Process Books (Generate Embeddings)
```bash
# Via API: POST /api/books/{id}/process/
curl -X POST http://localhost:8000/api/books/1/process/
```

### 3. Browse Books
Visit `http://localhost:3000/books` to see the book collection

### 4. View Book Details
Click on any book to see:
- Full description
- AI-generated summary
- Genre classification
- Sentiment analysis
- Recommendations

### 5. Ask Questions
Go to `http://localhost:3000/qa` and ask questions about the books:
- "What are the main themes?"
- "Which book discusses philosophy?"
- "What's the most romantic book?"

## API Documentation

### Books
```bash
# List all books
curl http://localhost:8000/api/books/

# Get book details
curl http://localhost:8000/api/books/1/

# Create a new book
curl -X POST http://localhost:8000/api/books/ \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Book Title",
    "author": "Author Name",
    "description": "Book description...",
    "rating": 4.5
  }'

# Process book (generate embeddings)
curl -X POST http://localhost:8000/api/books/1/process/

# Get AI insights
curl http://localhost:8000/api/books/1/insights/

# Get similar books
curl http://localhost:8000/api/books/1/recommendations/
```

### RAG Query
```bash
# Ask a question
curl -X POST http://localhost:8000/api/rag/query/ \
  -H "Content-Type: application/json" \
  -d '{
    "question": "What are the main themes in the books?"
  }'

# Ask about specific books
curl -X POST http://localhost:8000/api/rag/query/ \
  -H "Content-Type: application/json" \
  -d '{
    "question": "Compare the main characters",
    "book_ids": [1, 2, 3]
  }'
```

## Configuration

### Environment Variables

**Backend (.env)**:
```env
SECRET_KEY=your-secret-key
DEBUG=True
DB_NAME=book_insights
DB_USER=root
DB_PASSWORD=your-password
DB_HOST=127.0.0.1
OPENAI_API_KEY=your-api-key  # or use LM Studio
CORS_ALLOWED_ORIGINS=http://localhost:3000
```

**Frontend (.env.local)**:
```env
NEXT_PUBLIC_API_URL=http://localhost:8000
```

## Using Local LLM (LM Studio)

Instead of OpenAI:

1. Download [LM Studio](https://lmstudio.ai/)
2. Download a model (e.g., Mistral 7B)
3. Start the local server
4. Update `backend/rag/llm.py` to use `http://localhost:1234`

## Database Models

### Book
- `id`: Primary key
- `title`: Book title
- `author`: Author name
- `description`: Full description
- `rating`: Book rating (0-5)
- `url`: Source URL
- `cover_image`: Cover image URL
- `uploaded_at`: Timestamp
- `processed`: Whether embeddings are generated

### BookChunk
- `id`: Primary key
- `book_id`: Foreign key to Book
- `text`: Chunk content
- `embedding`: Vector embedding (JSON)
- `chunk_index`: Position in book
- `created_at`: Timestamp

### BookInsight
- `id`: Primary key
- `book_id`: Foreign key to Book
- `summary`: AI summary
- `genres`: Genre list (JSON)
- `sentiment`: Sentiment analysis
- `recommendations`: Similar book IDs (JSON)
- `created_at`, `updated_at`: Timestamps

### UserQuery
- `id`: Primary key
- `question`: User's question
- `answer`: AI-generated answer
- `sources`: Books used as context (JSON)
- `created_at`: Timestamp

## Advanced Features

### Chunking Strategies
The RAG pipeline includes configurable chunking:
- **Size**: 500 characters default (configurable)
- **Overlap**: 100 characters to maintain context
- Can be customized in `backend/rag/pipeline.py`

### Embedding Models
Currently using `all-MiniLM-L6-v2` (384-dim):
- Fast and efficient
- Good for semantic search
- Can be upgraded to `all-mpnet-base-v2` for better quality

### Vector Store
ChromaDB with:
- Persistent storage
- Cosine similarity search
- Metadata filtering
- Local or cloud deployment

## Troubleshooting

### Connection Refused
```bash
# Make sure both servers are running
# Backend: python manage.py runserver
# Frontend: npm run dev
# Check API URL in .env.local
```

### No Books Showing
```bash
# Load sample data
python manage.py shell < backend/scripts/sample_data.py

# Check if database migrations ran
python manage.py migrate
```

### RAG Query Fails
```bash
# Ensure books are processed
curl -X POST http://localhost:8000/api/books/1/process/

# Check OpenAI key or LM Studio running
# Verify embedding generation in backend logs
```

## Deployment

### Backend
```bash
# Heroku
heroku create your-app-name
heroku addons:create cleardb:ignite
git push heroku main

# Railway
railway init
railway add
railway up
```

### Frontend
```bash
# Vercel (recommended)
vercel
# Update NEXT_PUBLIC_API_URL to production backend URL
```

## Contributing

Contributions welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## License

MIT License - see LICENSE file for details

## Support

For issues or questions:
1. Check the [SETUP.md](./SETUP.md) guide
2. Review [backend README](./backend/README.md)
3. Check GitHub issues
4. Contact the development team

## Future Enhancements

- User authentication and accounts
- Favorite/bookmark system
- Advanced search filters
- Chat history persistence
- Custom reading lists
- Social sharing
- Mobile app
- Advanced semantic chunking
- Multi-language support
- Fine-tuned embedding models
- Caching layer (Redis)
- Real-time updates (WebSockets)

## Acknowledgments

- [Django](https://www.djangoproject.com/)
- [Next.js](https://nextjs.org/)
- [Sentence Transformers](https://www.sbert.net/)
- [ChromaDB](https://www.trychroma.com/)
- [shadcn/ui](https://ui.shadcn.com/)
- [Tailwind CSS](https://tailwindcss.com/)


