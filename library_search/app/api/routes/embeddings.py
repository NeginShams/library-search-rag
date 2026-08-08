# app/api/routes/embeddings.py
from fastapi import APIRouter

from app.schemas.embedding import EmbeddingRequest, EmbeddingResponse
from app.database.weaviate_client import embedding_service

router = APIRouter(
    prefix="/embeddings",
    tags=["Embeddings"],
)

@router.post("", response_model=EmbeddingResponse)
def generate_embedding(request: EmbeddingRequest):
    embedding = embedding_service.embed_query(request.text)
    return EmbeddingResponse(dimension=len(embedding), embedding=embedding)