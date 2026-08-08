from sentence_transformers import SentenceTransformer

from app.config import settings


class EmbeddingService:
    """
    Generates embeddings using the configured embedding model.

    This service is independent of Elasticsearch and Weaviate.
    It receives text and returns vectors.
    """

    def __init__(self):
        self.model = SentenceTransformer(
            settings.embedding_model,
            trust_remote_code=True,
            device=settings.embedding_device,
        )

    def embed_document(self, text: str) -> list[float]:
        """
        Generate an embedding for a single library page.

        A page is treated as one document/chunk in the RAG pipeline.
        """

        embedding = self.model.encode(
            text,
            task="retrieval",
            prompt_name="document",
            normalize_embeddings=True,
        )

        return embedding.tolist()

    def embed_documents(
        self,
        texts: list[str],
    ) -> list[list[float]]:
        """
        Generate embeddings for multiple library pages.

        Used during bulk ingestion from Elasticsearch into Weaviate.
        """

        embeddings = self.model.encode(
            texts,
            task="retrieval",
            prompt_name="document",
            batch_size=settings.embedding_batch_size,
            normalize_embeddings=True,
            show_progress_bar=False,
        )

        return embeddings.tolist()

    def embed_query(self, text: str) -> list[float]:
        """
        Generate an embedding for a user's search query.
        """

        embedding = self.model.encode(
            text,
            task="retrieval",
            prompt_name="query",
            normalize_embeddings=True,
        )

        return embedding.tolist()

    @property
    def dimension(self) -> int:
        """
        Return the dimensionality of the generated embeddings.
        """

        return self.model.get_sentence_embedding_dimension()
