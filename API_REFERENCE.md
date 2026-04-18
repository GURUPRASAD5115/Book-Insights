# API Reference

Complete documentation for the Book Insight Platform REST API.

## Base URL

```
http://localhost:8000/api
```

## Authentication

Currently, no authentication is required. Authentication can be added using Django's Token Authentication or JWT.

## Response Format

All responses are in JSON format.

### Success Response
```json
{
  "id": 1,
  "title": "Book Title",
  "author": "Author Name",
  ...
}
```

### Error Response
```json
{
  "error": "Error message",
  "detail": "More details about the error"
}
```

## Books Endpoints

### List All Books

**GET** `/api/books/`

Returns a paginated list of all books.

**Query Parameters:**
- `page` (optional): Page number (default: 1)
- `page_size` (optional): Items per page (default: 12)

**Example:**
```bash
curl http://localhost:8000/api/books/
curl http://localhost:8000/api/books/?page=2&page_size=20
```

**Response:**
```json
{
  "count": 50,
  "next": "http://localhost:8000/api/books/?page=2",
  "previous": null,
  "results": [
    {
      "id": 1,
      "title": "To Kill a Mockingbird",
      "author": "Harper Lee",
      "description": "A gripping tale...",
      "rating": 4.8,
      "url": "https://...",
      "cover_image": "https://...",
      "uploaded_at": "2024-01-15T10:30:00Z",
      "processed": true,
      "chunks": [...],
      "insight": {...}
    },
    ...
  ]
}
```

**Status:** `200 OK`

---

### Get Book Details

**GET** `/api/books/{id}/`

Returns detailed information about a specific book.

**Parameters:**
- `id` (required): Book ID

**Example:**
```bash
curl http://localhost:8000/api/books/1/
```

**Response:**
```json
{
  "id": 1,
  "title": "To Kill a Mockingbird",
  "author": "Harper Lee",
  "description": "A gripping tale...",
  "rating": 4.8,
  "url": "https://...",
  "cover_image": "https://...",
  "uploaded_at": "2024-01-15T10:30:00Z",
  "processed": true,
  "chunks": [
    {
      "id": 101,
      "text": "The first chunk of text...",
      "chunk_index": 0
    },
    ...
  ],
  "insight": {
    "id": 1,
    "summary": "A powerful story about injustice...",
    "genres": ["Literary Fiction", "Drama", "Classics"],
    "sentiment": "neutral",
    "recommendations": [2, 3, 5]
  }
}
```

**Status:** `200 OK`

---

### Create a Book

**POST** `/api/books/`

Create a new book entry.

**Request Body:**
```json
{
  "title": "New Book Title",
  "author": "Author Name",
  "description": "Book description",
  "rating": 4.5,
  "url": "https://example.com/book",
  "cover_image": "https://example.com/image.jpg"
}
```

**Required Fields:**
- `title`: String, max 255 characters
- `author`: String, max 255 characters
- `description`: String

**Optional Fields:**
- `rating`: Float, 0-5
- `url`: URL
- `cover_image`: URL

**Example:**
```bash
curl -X POST http://localhost:8000/api/books/ \
  -H "Content-Type: application/json" \
  -d '{
    "title": "The Great Gatsby",
    "author": "F. Scott Fitzgerald",
    "description": "A novel about the Jazz Age...",
    "rating": 4.5
  }'
```

**Response:**
```json
{
  "id": 7,
  "title": "The Great Gatsby",
  "author": "F. Scott Fitzgerald",
  "description": "A novel about the Jazz Age...",
  "rating": 4.5,
  "url": null,
  "cover_image": null,
  "uploaded_at": "2024-01-20T14:22:00Z",
  "processed": false,
  "chunks": [],
  "insight": null
}
```

**Status:** `201 Created`

---

### Update a Book

**PUT** `/api/books/{id}/`

Update all fields of a book.

**Parameters:**
- `id` (required): Book ID

**Request Body:** Same as Create

**Status:** `200 OK`

---

### Partially Update a Book

**PATCH** `/api/books/{id}/`

Update specific fields of a book.

**Status:** `200 OK`

---

### Delete a Book

**DELETE** `/api/books/{id}/`

Delete a book and its associated data.

**Status:** `204 No Content`

---

### Process a Book

**POST** `/api/books/{id}/process/`

Generate embeddings for a book. This creates chunks and stores vector embeddings in ChromaDB.

**Parameters:**
- `id` (required): Book ID

**Example:**
```bash
curl -X POST http://localhost:8000/api/books/1/process/
```

**Response:**
```json
{
  "status": "Book processed successfully"
}
```

**Status:** `200 OK`

**Notes:**
- This operation may take 10-30 seconds depending on book length
- Must be called before using RAG queries with this book
- Can only process books with description text

---

### Get Book Insights

**GET** `/api/books/{id}/insights/`

Get AI-generated insights for a book (summary, genres, sentiment).

**Parameters:**
- `id` (required): Book ID

**Example:**
```bash
curl http://localhost:8000/api/books/1/insights/
```

**Response:**
```json
{
  "id": 1,
  "book": 1,
  "summary": "A powerful story about racial injustice in the American South...",
  "genres": ["Literary Fiction", "Drama", "Classics"],
  "sentiment": "serious",
  "recommendations": [2, 3, 5],
  "created_at": "2024-01-15T10:35:00Z",
  "updated_at": "2024-01-15T10:35:00Z"
}
```

**Status:** `200 OK`

**Notes:**
- Returns 404 if book hasn't been processed yet
- Insights are generated during the process step

---

### Get Book Recommendations

**GET** `/api/books/{id}/recommendations/`

Get similar books based on embedding similarity.

**Parameters:**
- `id` (required): Book ID

**Example:**
```bash
curl http://localhost:8000/api/books/1/recommendations/
```

**Response:**
```json
[
  {
    "id": 3,
    "title": "Moby Dick",
    "author": "Herman Melville",
    ...
  },
  {
    "id": 5,
    "title": "Jane Eyre",
    "author": "Charlotte Brontë",
    ...
  }
]
```

**Status:** `200 OK`

**Notes:**
- Returns up to 3 similar books
- Uses cosine similarity of embeddings
- Book must be processed to get recommendations

---

## RAG Query Endpoint

### Query Books with RAG

**POST** `/api/rag/query/`

Ask a question about the books. The system will search for relevant content and generate an AI answer.

**Request Body:**
```json
{
  "question": "What are the main themes?",
  "book_ids": [1, 2, 3]
}
```

**Fields:**
- `question` (required): String, max 1000 characters
- `book_ids` (optional): Array of book IDs to search in. If omitted, searches all books.

**Example 1: Query all books**
```bash
curl -X POST http://localhost:8000/api/rag/query/ \
  -H "Content-Type: application/json" \
  -d '{
    "question": "What are the main themes explored in these books?"
  }'
```

**Example 2: Query specific books**
```bash
curl -X POST http://localhost:8000/api/rag/query/ \
  -H "Content-Type: application/json" \
  -d '{
    "question": "Compare the main characters",
    "book_ids": [1, 2, 3]
  }'
```

**Response:**
```json
{
  "question": "What are the main themes?",
  "answer": "The main themes include injustice, innocence, and courage. Throughout the books, characters grapple with moral questions about right and wrong...",
  "sources": [1, 3, 5],
  "query_id": 42
}
```

**Status:** `200 OK`

**Error Response (400 Bad Request):**
```json
{
  "error": "LLM Manager not available. Please configure OpenAI API key."
}
```

**Notes:**
- Requires at least one processed book
- Sources list contains IDs of books used for context
- LLM must be configured (OpenAI or LM Studio)
- Answers are generated using retrieved chunks as context
- Response time: 2-5 seconds

---

## Insights Endpoints

### List All Insights

**GET** `/api/insights/`

Get AI insights for all books.

**Response:**
```json
{
  "count": 6,
  "results": [
    {
      "id": 1,
      "book": 1,
      "summary": "...",
      "genres": ["Fiction", "Drama"],
      "sentiment": "serious",
      "recommendations": [2, 3],
      "created_at": "2024-01-15T10:35:00Z",
      "updated_at": "2024-01-15T10:35:00Z"
    },
    ...
  ]
}
```

**Status:** `200 OK`

---

### Generate Insights for All Books

**POST** `/api/insights/generate_insights/`

Generate AI insights for all unprocessed books.

**Example:**
```bash
curl -X POST http://localhost:8000/api/insights/generate_insights/
```

**Response:**
```json
{
  "status": "Generated insights for 3 books"
}
```

**Status:** `200 OK`

---

## Error Codes

| Code | Meaning | Description |
|------|---------|-------------|
| 200 | OK | Successful GET/POST |
| 201 | Created | Resource successfully created |
| 204 | No Content | Successful DELETE |
| 400 | Bad Request | Invalid request parameters |
| 404 | Not Found | Resource not found |
| 500 | Server Error | Internal server error |

## Rate Limiting

Currently no rate limiting is implemented. It can be added using Django REST Framework throttling.

## Pagination

List endpoints support pagination with:
- `page`: Page number (default: 1)
- `page_size`: Items per page (default: 12)

**Example:**
```bash
curl http://localhost:8000/api/books/?page=2&page_size=20
```

## Data Types

### Book Object
```json
{
  "id": 1,
  "title": "string",
  "author": "string",
  "description": "string",
  "rating": 4.5,
  "url": "string or null",
  "cover_image": "string or null",
  "uploaded_at": "ISO 8601 datetime",
  "processed": true,
  "chunks": [...],
  "insight": {...}
}
```

### Insight Object
```json
{
  "id": 1,
  "book": 1,
  "summary": "string or null",
  "genres": ["string"],
  "sentiment": "string or null",
  "recommendations": [1, 2, 3],
  "created_at": "ISO 8601 datetime",
  "updated_at": "ISO 8601 datetime"
}
```

### Query Response Object
```json
{
  "question": "string",
  "answer": "string",
  "sources": [1, 2, 3],
  "query_id": 42
}
```

## Testing with curl

### List books
```bash
curl http://localhost:8000/api/books/
```

### Get specific book
```bash
curl http://localhost:8000/api/books/1/
```

### Create book
```bash
curl -X POST http://localhost:8000/api/books/ \
  -H "Content-Type: application/json" \
  -d '{"title":"Test","author":"Author","description":"Desc"}'
```

### Process book
```bash
curl -X POST http://localhost:8000/api/books/1/process/
```

### Get insights
```bash
curl http://localhost:8000/api/books/1/insights/
```

### Query with RAG
```bash
curl -X POST http://localhost:8000/api/rag/query/ \
  -H "Content-Type: application/json" \
  -d '{"question":"What are the themes?"}'
```

## Frontend Integration Example

```javascript
// Fetch books
const response = await fetch('http://localhost:8000/api/books/');
const data = await response.json();

// Get book details
const bookResponse = await fetch('http://localhost:8000/api/books/1/');
const book = await bookResponse.json();

// Query with RAG
const queryResponse = await fetch('http://localhost:8000/api/rag/query/', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    question: 'What are the main themes?',
    book_ids: [1, 2]
  })
});
const result = await queryResponse.json();
```

## Changelog

### v1.0.0
- Initial release
- All core endpoints implemented
- RAG query support
- Insight generation

## Future Endpoints

Planned for future versions:
- User authentication
- Favorites/Bookmarks
- Reading lists
- Comments and reviews
- Advanced search filters
- User profiles
