from app.config import settings
from app.services.embedding_service import EmbeddingService
from app.services.weaviate_service import WeaviateService


class RetrievalService:
    """
    Service responsible for retrieving relevant library pages.
    """

    def __init__(
        self,
        embedding_service: EmbeddingService,
        weaviate_service: WeaviateService,
    ):
        self.embedding_service = embedding_service
        self.weaviate_service = weaviate_service

    def search(
        self,
        query: str,
    ) -> list[dict]:
        """
        Retrieve relevant library pages using hybrid search.

        Hybrid retrieval combines:

            40% dense/vector retrieval
            60% BM25 retrieval
        """

        if not query or not query.strip():
            raise ValueError(
                "Query cannot be empty."
            )

        query = query.strip()

        # ---------------------------------------------
        # 1. Generate query embedding
        # ---------------------------------------------

        query_vector = (
            self.embedding_service.embed_query(
                query
            )
        )

        # ---------------------------------------------
        # 2. Hybrid retrieval
        # ---------------------------------------------

        results = (
            self.weaviate_service.hybrid_search(
                query=query,
                vector=query_vector,
                limit=settings.retrieval_top_k,
            )
        )

        return results