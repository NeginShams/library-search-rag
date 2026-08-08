# Library Search API

A FastAPI-based embedding and retrieval service for an online digital library.

The service is responsible for:

* Generating text embeddings using **Jina AI `jina-embeddings-v5-text-nano-retrieval`**
* Storing library pages and their embeddings in **Weaviate**
* Performing dense vector search
* Performing BM25 keyword search
* Performing hybrid search using dense + BM25 retrieval
* Indexing individual pages or batches of pages
* Managing indexed library pages

The LLM-based answer generation layer is **outside the scope of this service** and is handled by another component/team.

---

## Architecture

```text
                    Library Search API
                           │
                     ┌─────┴─────┐
                     │  FastAPI  │
                     └─────┬─────┘
                           │
          ┌────────────────┼────────────────┐
          │                │                │
     Embeddings        Documents          Search
          │                │                │
          ▼                ▼                ▼
   EmbeddingService   WeaviateService   RetrievalService
          │                │                │
          │                ▼                │
          │            Weaviate ◄───────────┘
          │
          ▼
       Jina AI
   Embedding Model
```

---

## Data Model

The original library data is stored in JSON files.

Each library page is treated as **one chunk**.

A page contains information such as:

```text
page_id
book_id
page_num
title
content
```

The relationship is:

```text
Book
 │
 ├── Page 1
 ├── Page 2
 ├── Page 3
 └── ...
```

Each page is independently embedded and indexed in Weaviate.

---

## Technologies

* Python
* FastAPI
* Uvicorn
* Weaviate
* Docker
* Sentence Transformers
* Jina AI embeddings
* Pydantic

### Embedding model

```text
jinaai/jina-embeddings-v5-text-nano-retrieval
```

The model currently produces **768-dimensional embeddings**.

---

## Project Structure

```text
library_search/
│
├── app/
│   ├── main.py
│   ├── config.py
│   │
│   ├── api/
│   │   └── routes/
│   │       ├── health.py
│   │       ├── embeddings.py
│   │       ├── documents.py
│   │       └── search.py
│   │
│   ├── schemas/
│   │   ├── embedding.py
│   │   ├── document.py
│   │   └── search.py
│   │
│   ├── services/
│   │   ├── embedding_service.py
│   │   ├── weaviate_service.py
│   │   └── retrieval_service.py
│   │
│   └── database/
│       └── weaviate_client.py
│
├── test/
│   ├── test_embedding.py
│   ├── test_weaviate.py
│   └── test_ingestion.py
│
├── data/
│   └── ...
│
├── docker-compose.yml
├── requirements.txt
└── README.md
```

---

# Setup

## 1. Create a virtual environment

Windows:

```bash
python -m venv myenv
```

Activate it:

```bash
myenv\Scripts\activate
```

---

## 2. Install dependencies

```bash
pip install -r requirements.txt
```

If `requirements.txt` has not been created yet, the main dependencies are:

```text
fastapi
uvicorn
weaviate-client
sentence-transformers
pydantic
pydantic-settings
torch
```

---

# Weaviate

Weaviate runs separately from the FastAPI application using Docker.

Start Weaviate with:

```bash
docker compose up -d
```

Check running containers:

```bash
docker ps
```

Stop Weaviate:

```bash
docker compose down
```

The application connects to the local Weaviate instance through the Weaviate client.

---

# Configuration

Application configuration is stored in `app/config.py`.

Important configuration values include:

```text
Embedding model
Embedding device
Embedding batch size

Weaviate host/connection settings

Retrieval top-k
Dense weight
BM25 weight
Weaviate alpha
```

Current retrieval configuration:

```text
Top-K          = 5
Dense weight   = 0.4
BM25 weight    = 0.6
Alpha          = 0.4
```

The configuration should be changed through the configuration/environment layer rather than hard-coded inside services.

---

# Running the API

Start the FastAPI application:

```bash
uvicorn app.main:app
```

For development:

```bash
uvicorn app.main:app --reload
```

The API will be available at:

```text
http://127.0.0.1:8000
```

Interactive Swagger documentation:

```text
http://127.0.0.1:8000/docs
```

---

# API Endpoints

## Health Check

### `GET /health`

Checks whether the API is running.

Example response:

```json
{
  "status": "ok"
}
```

---

# Embeddings

## `POST /embeddings`

Generates an embedding for a text query.

Request:

```json
{
  "text": "این کتاب درباره تاریخ ایران است."
}
```

Response:

```json
{
  "dimension": 768,
  "embedding": [
    0.0123,
    -0.0345
  ]
}
```

The complete embedding vector contains 768 values.

---

# Documents

## `POST /documents`

Indexes a single library page.

A page is treated as one chunk.

Request:

```json
{
  "page_id": 103020,
  "book_id": 359010,
  "page_num": 20149,
  "title": "بانک جامع فهرست الفبایی نسخ خطی جهان جلد 2 حرف ا",
  "content": "الحصن الحصین من کلام سید المرسلین..."
}
```

The service:

1. Receives the page.
2. Generates its document embedding.
3. Stores the page and embedding in Weaviate.
4. Returns the Weaviate UUID.

Example response:

```json
{
  "page_id": 103020,
  "uuid": "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx"
}
```

---

## `POST /documents/batch`

Indexes multiple library pages.

Request:

```json
{
  "documents": [
    {
      "page_id": 1,
      "book_id": 100,
      "page_num": 1,
      "title": "کتاب آزمایشی",
      "content": "..."
    },
    {
      "page_id": 2,
      "book_id": 100,
      "page_num": 2,
      "title": "کتاب آزمایشی",
      "content": "..."
    }
  ]
}
```

The pages are embedded using batch encoding before being inserted into Weaviate.

Example response:

```json
{
  "inserted": 2,
  "failed": 0,
  "uuids": [
    "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx",
    "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx"
  ]
}
```

This endpoint is intended for large-scale ingestion when the application is deployed on the company server.

---

## `GET /documents/{page_id}`

Retrieves an indexed page.

Example:

```text
GET /documents/103020
```

---

## `DELETE /documents/{page_id}`

Deletes an indexed page from Weaviate.

Example:

```text
DELETE /documents/103020
```

Response:

```json
{
  "page_id": 103020,
  "deleted": true
}
```

---

# Search

## `POST /search`

Performs hybrid retrieval.

Request:

```json
{
  "query": "الحصن الحصین درباره چیست؟"
}
```

The retrieval process is:

```text
User Query
    │
    ▼
Query Embedding
    │
    ▼
Hybrid Search
   / \
  /   \
Dense  BM25
0.4    0.6
  \   /
   \ /
    ▼
 Top-K Results
```

Current configuration:

```text
Top-K        = 5
Dense weight = 0.4
BM25 weight  = 0.6
```

The endpoint returns the most relevant library pages.

Example response:

```json
{
  "query": "الحصن الحصین درباره چیست؟",
  "results": [
    {
      "page_id": 103020,
      "book_id": 359010,
      "page_num": 20149,
      "title": "بانک جامع فهرست الفبایی نسخ خطی جهان جلد 2 حرف ا",
      "content": "...",
      "score": 0.123
    }
  ]
}
```

---

# Retrieval Pipeline

The retrieval pipeline is intentionally independent from LLM generation.

```text
                    Query
                      │
                      ▼
              EmbeddingService
                      │
                      ▼
               Query Embedding
                      │
                      ▼
              RetrievalService
                      │
                      ▼
                 Weaviate
                /         \
               /           \
          Vector Search    BM25
             0.4            0.6
               \           /
                \         /
                 Hybrid Search
                      │
                      ▼
                   Top-K
                      │
                      ▼
               Relevant Pages
```

The resulting pages can then be passed to the separate RAG/LLM component.

---

# Testing

Individual components can be tested before running the complete API.

## Test embedding service

```bash
python test/test_embedding.py
```

## Test Weaviate

```bash
python test/test_weaviate.py
```

## Test ingestion

```bash
python test/test_ingestion.py
```

---

# Current Development Environment

The system is currently being tested locally on Windows.

```text
Windows
   │
   ├── FastAPI
   │
   ├── Jina embedding model
   │
   └── Docker
        │
        └── Weaviate
```

The current local environment is intended for development and testing with a relatively small number of pages.

Large-scale ingestion will be performed after deployment to the company server.

---

# Responsibilities

This service is responsible for:

* Text embedding
* Document embedding
* Page indexing
* Vector storage
* Dense retrieval
* BM25 retrieval
* Hybrid retrieval
* Returning relevant library pages

The following are outside the scope of this service:

* LLM inference
* Prompt construction for answer generation
* Final answer generation
* Conversational response generation

These responsibilities belong to the separate RAG/LLM component.

---

# Future Improvements

Potential future improvements include:

* Production deployment
* Batch ingestion optimization
* Better error handling
* Authentication and authorization
* Logging
* Monitoring
* Retrieval evaluation
* Retrieval metrics such as Recall@K and MRR
* Re-ranking
* Metadata filtering
* Improved hybrid-search tuning
* Weaviate index optimization
* Async/background ingestion
* API versioning
* Automated tests

