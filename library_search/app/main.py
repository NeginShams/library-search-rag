from fastapi import FastAPI

from app.api.routes import (
    health,
    embeddings,
    documents,
    search,
)


app = FastAPI(
    title="Library Search API",
    description="Embedding and retrieval API for the online library",
    version="1.0.0",
)


app.include_router(
    health.router
)

app.include_router(
    embeddings.router
)

app.include_router(
    documents.router
)

app.include_router(
    search.router
)