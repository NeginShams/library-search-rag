# app/api/routes/search.py
from fastapi import APIRouter

from app.schemas.search import (
    SearchRequest,
    SearchResponse,
    SearchResult,
)

from app.services.retrieval_service import RetrievalService
from app.services.embedding_service import EmbeddingService
from app.services.weaviate_service import WeaviateService
from app.database.weaviate_client import client


router = APIRouter(
    prefix="/search",
    tags=["Search"],
)

# ← Instantiate dependencies first, then pass them in
embedding_service = EmbeddingService()
weaviate_service  = WeaviateService(client=client)
retrieval_service = RetrievalService(
    embedding_service=embedding_service,
    weaviate_service=weaviate_service,
)


@router.post("", response_model=SearchResponse)
def search(request: SearchRequest):

    results = retrieval_service.search(
        query=request.query
    )

    return SearchResponse(
        query=request.query,
        results=[
            SearchResult(
                page_id=result["page_id"],
                book_id=result["book_id"],
                page_num=result["page_num"],
                title=result["title"],
                content=result["content"],
                score=result.get("score"),
            )
            for result in results
        ],
    )